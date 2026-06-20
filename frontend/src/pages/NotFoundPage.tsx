import { Link } from "react-router-dom";
import { Button } from "@/components/ui";

export function NotFoundPage() {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-24 text-center">
      <p className="font-mono text-4xl font-semibold text-brand-500">404</p>
      <p className="text-sm text-slate-400">This page does not exist.</p>
      <Link to="/">
        <Button variant="secondary">Back to dashboard</Button>
      </Link>
    </div>
  );
}
