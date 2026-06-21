import type { ReactNode } from "react";
import type { UseQueryResult } from "@tanstack/react-query";
import { Card, EmptyState, ErrorState, Loading, Table, Td, Th } from "@/components/ui";

export interface Column<T> {
  header: string;
  render: (row: T) => ReactNode;
}

interface ResourceTableProps<T> {
  query: UseQueryResult<T[], unknown>;
  columns: Column<T>[];
  rowKey: (row: T) => string;
  emptyTitle: string;
  toolbar?: ReactNode;
}

// Generic list view driven by a query + column config. Used by every
// read-only sub-resource tab to avoid duplicating fetch/empty/error logic.
export function ResourceTable<T>({ query, columns, rowKey, emptyTitle, toolbar }: ResourceTableProps<T>) {
  const { data, isLoading, error } = query;
  const countLabel = data ? `${data.length} ${data.length === 1 ? "record" : "records"}` : null;

  return (
    <div className="space-y-4">
      {(countLabel || toolbar) && (
        <div className="flex items-center justify-between gap-3">
          {countLabel ? <span className="text-xs text-slate-500">{countLabel}</span> : <span />}
          {toolbar}
        </div>
      )}
      {isLoading && <Loading />}
      {error ? <ErrorState error={error} /> : null}
      {data && data.length === 0 && <EmptyState title={emptyTitle} />}
      {data && data.length > 0 && (
        <Card>
          <Table>
            <thead>
              <tr>
                {columns.map((c) => (
                  <Th key={c.header}>{c.header}</Th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-ink-800">
              {data.map((row) => (
                <tr key={rowKey(row)} className="hover:bg-ink-700/30">
                  {columns.map((c) => (
                    <Td key={c.header}>{c.render(row)}</Td>
                  ))}
                </tr>
              ))}
            </tbody>
          </Table>
        </Card>
      )}
    </div>
  );
}
