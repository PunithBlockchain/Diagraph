import { Plugin } from "@elizaos/core";
import { GraphQueryAction } from "./actions/graphQuery";
import { GraphService } from "./service";
import { GraphProvider } from "./providers/graphProvider";

export const diagraphPlugin: Plugin = {
  name: "diagraph-plugin",
  description: "Enables Eliza agents to query DiaGraph knowledge graphs and log provenance to Solana",
  actions: [GraphQueryAction],
  providers: [GraphProvider],
  services: [GraphService],
};