import { useSafetySummary } from "@/hooks/queries";
import { Badge, Card, CardBody, CardHeader, ErrorState, Loading } from "@/components/ui";
import { humanize } from "@/lib/format";

export function SafetyTab({ projectId }: { projectId: string }) {
  const { data, isLoading, error } = useSafetySummary(projectId);

  if (isLoading) return <Loading />;
  if (error) return <ErrorState error={error} />;
  if (!data) return null;

  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <Card>
        <CardHeader title="Scope gate" subtitle="Asset and campaign creation is blocked without an approved scope." />
        <CardBody>
          <div className="flex items-center gap-3">
            {data.has_approved_scope ? (
              <Badge tone="green">Approved scope active</Badge>
            ) : (
              <Badge tone="red">No approved scope</Badge>
            )}
            <span className="text-sm text-slate-400">
              {data.approved_scope_count} approved scope{data.approved_scope_count === 1 ? "" : "s"}
            </span>
          </div>
          {!data.has_approved_scope && (
            <p className="mt-3 text-sm text-slate-500">
              Approve at least one scope before registering in-scope assets or launching campaigns.
            </p>
          )}
        </CardBody>
      </Card>

      <Card>
        <CardHeader title="Restricted actions" subtitle="Aggregated across approved scopes." />
        <CardBody>
          {data.restricted_actions.length === 0 ? (
            <p className="text-sm text-slate-500">No restricted actions declared.</p>
          ) : (
            <div className="flex flex-wrap gap-2">
              {data.restricted_actions.map((a) => (
                <Badge key={a} tone="amber">
                  {humanize(a)}
                </Badge>
              ))}
            </div>
          )}
        </CardBody>
      </Card>
    </div>
  );
}
