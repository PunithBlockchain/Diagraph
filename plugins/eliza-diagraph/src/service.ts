import { Service, IAgentRuntime } from "@elizaos/core";
import axios from "axios";
import * as anchor from "@project-serum/anchor";
import { Connection, PublicKey } from "@solana/web3.js";

export class GraphService extends Service {
  static serviceType = "diagraph";
  capabilityDescription = "Connects to DiaGraph FastAPI backend and Solana blockchain";
  private fastApiUrl: string;
  private solanaRpc: string;
  private programId: PublicKey;

  constructor(protected runtime: IAgentRuntime) {
    super();
    this.fastApiUrl = process.env.FASTAPI_URL || "http://localhost:8000";
    this.solanaRpc = process.env.SOLANA_RPC || "http://localhost:8899";
    this.programId = new PublicKey(process.env.PROGRAM_ID || "11111111111111111111111111111111");
  }

  static async start(runtime: IAgentRuntime): Promise<GraphService> {
    const service = new GraphService(runtime);
    return service;
  }

  async stop(): Promise<void> {
    // Clean up resources if needed
  }

  async fetchGraphData(): Promise<any> {
    try {
      const response = await axios.get(`${this.fastApiUrl}/graph`);
      return response.data;
    } catch (error) {
      console.error("Error fetching graph data:", error);
      throw error;
    }
  }

  async logProvenance(source: string, id: string, hash: string): Promise<void> {
    const connection = new Connection(this.solanaRpc, "confirmed");
    const provider = anchor.getProvider();
    const program = new anchor.Program({}, this.programId, provider);
    await program.rpc.logData(source, id, hash, {
      accounts: {},
      signers: [],
    });
  }
}