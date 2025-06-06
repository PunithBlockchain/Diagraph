import { Provider, IAgentRuntime, Memory } from "@elizaos/core";
import { GraphService } from "../service";

export const GraphProvider: Provider = {
  name: "graph-provider",
  description: "Provides context from DiaGraph knowledge graph",
  getContext: async (runtime: IAgentRuntime, message: Memory) => {
    const service = runtime.getService("diagraph") as GraphService;
    const graphData = await service.fetchGraphData();
    return {
      context: `Graph contains ${graphData.nodes.length} nodes (e.g., ${graphData.nodes[0].data.label}) and ${graphData.edges.length} edges.`,
    };
  },
};