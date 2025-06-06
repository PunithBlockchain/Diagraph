import { Action, IAgentRuntime, Memory } from "@elizaos/core";
import { GraphService } from "../service";

export const GraphQueryAction: Action = {
  name: "GRAPH_QUERY",
  similes: ["FETCH_GRAPH", "QUERY_KNOWLEDGE"],
  validate: async (runtime: IAgentRuntime, message: Memory) => {
    return message.content.text.includes("graph") || message.content.text.includes("query");
  },
  handler: async (runtime: IAgentRuntime, message: Memory) => {
    const service = runtime.getService("diagraph") as GraphService;
    try {
      const graphData = await service.fetchGraphData();
      const response = `Found ${graphData.nodes.length} nodes and ${graphData.edges.length} edges. Example: ${graphData.nodes[0].data.label}`;
      await runtime.createMemory({
        content: { text: response },
        agentId: runtime.agentId,
        roomId: message.roomId,
      });
      return true;
    } catch (error) {
      console.error("Graph query failed:", error);
      return false;
    }
  },
  examples: [
    { input: "Query the knowledge graph", output: "Fetching graph data..." },
    { input: "Show me the graph", output: "Retrieving nodes and edges..." },
  ],
};