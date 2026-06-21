import { useMemo, useState } from "react";
import { useAttackTechniques } from "@/hooks/queries";
import { Badge, Card, EmptyState, ErrorState, Field, Input, Loading, Table, Td, Th } from "@/components/ui";
import { humanize } from "@/lib/format";

export function AttackPage() {
  const { data, isLoading, error } = useAttackTechniques();
  const [search, setSearch] = useState("");
  const filtered = useMemo(() => {
    const query = search.trim().toLowerCase();
    if (!query) return data ?? [];
    return (data ?? []).filter((technique) =>
      [
        technique.technique_id,
        technique.name,
        technique.source,
        ...technique.tactic_refs,
        ...technique.platforms,
      ]
        .join(" ")
        .toLowerCase()
        .includes(query),
    );
  }, [data, search]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold text-slate-100">ATT&CK techniques</h1>
        <p className="text-sm text-slate-500">Reference catalog exposed by the backend.</p>
      </div>

      {isLoading && <Loading />}
      {error && <ErrorState error={error} />}
      {data && data.length === 0 && <EmptyState title="No techniques available" />}

      {data && data.length > 0 && (
        <>
          <Field label="Search">
            <Input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Technique ID, name, tactic, platform, or source"
            />
          </Field>
          {filtered.length === 0 ? (
            <EmptyState title="No matching techniques" />
          ) : (
            <Card>
              <Table>
                <thead>
                  <tr>
                    <Th>ID</Th>
                    <Th>Name</Th>
                    <Th>Tactics</Th>
                    <Th>Platforms</Th>
                    <Th>Source</Th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-ink-800">
                  {filtered.map((t) => (
                    <tr key={t.technique_id} className="hover:bg-ink-700/30">
                      <Td>
                        <span className="font-mono text-xs text-brand-300">{t.technique_id}</span>
                      </Td>
                      <Td>
                        <span className="font-medium text-slate-100">{t.name}</span>
                      </Td>
                      <Td>
                        <span className="flex flex-wrap gap-1">
                          {t.tactic_refs.map((r) => (
                            <Badge key={r} tone="violet">
                              {humanize(r)}
                            </Badge>
                          ))}
                        </span>
                      </Td>
                      <Td>{t.platforms.join(", ") || "—"}</Td>
                      <Td>
                        <span className="text-xs text-slate-500">{t.source}</span>
                      </Td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </Card>
          )}
        </>
      )}
    </div>
  );
}
