from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import Role, User, UserRole
from app.schemas.auth import TokenResponse
from app.schemas.common import new_id, utc_now
from app.schemas.user import CurrentUser, UserCreate, UserRead, UserUpdate

DEFAULT_ROLES = {
    "admin": "Full administrative access.",
    "lead_operator": "Can manage projects, scopes, campaigns, and reports.",
    "operator": "Can work on assigned engagement data.",
    "reviewer": "Can review engagement data and reports.",
    "client_viewer": "Can view approved deliverables.",
}


def initialize_auth_defaults(db: Session) -> None:
    roles_by_name = {role.name: role for role in db.scalars(select(Role)).all()}
    for role_name, description in DEFAULT_ROLES.items():
        if role_name not in roles_by_name:
            role = Role(
                role_id=new_id("role"),
                name=role_name,
                description=description,
                created_at=utc_now(),
                updated_at=utc_now(),
            )
            db.add(role)
            roles_by_name[role_name] = role
    db.commit()

    if not settings.bootstrap_admin_enabled:
        return

    admin = db.scalar(select(User).where(User.email == settings.bootstrap_admin_email))
    if admin is None:
        admin = User(
            user_id=new_id("user"),
            email=settings.bootstrap_admin_email,
            full_name=settings.bootstrap_admin_full_name,
            password_hash=hash_password(settings.bootstrap_admin_password),
            is_active=True,
            created_at=utc_now(),
            updated_at=utc_now(),
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)

    admin_role = db.scalar(select(Role).where(Role.name == "admin"))
    if admin_role is None:
        return

    existing_link = db.scalar(
        select(UserRole).where(UserRole.user_id == admin.user_id, UserRole.role_id == admin_role.role_id)
    )
    if existing_link is None:
        db.add(
            UserRole(
                user_role_id=new_id("user_role"),
                user_id=admin.user_id,
                role_id=admin_role.role_id,
                created_at=utc_now(),
            )
        )
        db.commit()


def authenticate_user(db: Session, email: str, password: str) -> TokenResponse | None:
    user = db.scalar(select(User).where(User.email == email))
    if user is None or not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None

    user.last_login_at = utc_now()
    db.commit()
    roles = get_role_names(db, user.user_id)
    return TokenResponse(
        access_token=create_access_token(user.user_id, roles),
        expires_in=settings.access_token_expire_minutes * 60,
    )


def get_user_by_id(db: Session, user_id: str) -> CurrentUser | None:
    user = db.get(User, user_id)
    if user is None:
        return None
    return CurrentUser(
        user_id=user.user_id,
        email=user.email,
        full_name=user.full_name,
        roles=get_role_names(db, user.user_id),
        is_active=user.is_active,
    )


def list_users(db: Session) -> list[UserRead]:
    users = db.scalars(select(User).order_by(User.email)).all()
    return [user_to_read(db, user) for user in users]


def get_user_read(db: Session, user_id: str) -> UserRead | None:
    user = db.get(User, user_id)
    return user_to_read(db, user) if user else None


def create_user(db: Session, payload: UserCreate) -> UserRead:
    now = utc_now()
    user = User(
        user_id=new_id("user"),
        email=payload.email,
        full_name=payload.full_name,
        password_hash=hash_password(payload.password),
        is_active=payload.is_active,
        created_at=now,
        updated_at=now,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    set_user_roles(db, user.user_id, payload.roles)
    return user_to_read(db, user)


def update_user(db: Session, user_id: str, payload: UserUpdate) -> UserRead | None:
    user = db.get(User, user_id)
    if user is None:
        return None

    data = payload.model_dump(exclude_unset=True)
    if "full_name" in data:
        user.full_name = data["full_name"]
    if "password" in data:
        user.password_hash = hash_password(data["password"])
    if "is_active" in data:
        user.is_active = data["is_active"]
    user.updated_at = utc_now()
    db.commit()
    db.refresh(user)

    if "roles" in data:
        set_user_roles(db, user.user_id, data["roles"])

    return user_to_read(db, user)


def set_user_roles(db: Session, user_id: str, role_names: list[str]) -> None:
    roles = db.scalars(select(Role).where(Role.name.in_(role_names))).all()
    if len(roles) != len(set(role_names)):
        existing = {role.name for role in roles}
        missing = sorted(set(role_names) - existing)
        raise ValueError(f"Unknown roles: {', '.join(missing)}")

    for link in db.scalars(select(UserRole).where(UserRole.user_id == user_id)).all():
        db.delete(link)
    db.flush()

    for role in roles:
        db.add(
            UserRole(
                user_role_id=new_id("user_role"),
                user_id=user_id,
                role_id=role.role_id,
                created_at=utc_now(),
            )
        )
    db.commit()


def user_to_read(db: Session, user: User) -> UserRead:
    return UserRead(
        user_id=user.user_id,
        email=user.email,
        full_name=user.full_name,
        roles=get_role_names(db, user.user_id),
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
        last_login_at=user.last_login_at,
    )


def get_role_names(db: Session, user_id: str) -> list[str]:
    statement = (
        select(Role.name)
        .join(UserRole, UserRole.role_id == Role.role_id)
        .where(UserRole.user_id == user_id)
        .order_by(Role.name)
    )
    return list(db.scalars(statement).all())
