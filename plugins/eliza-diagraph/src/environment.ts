import { validateEnv } from "@elizaos/core";

export const env = validateEnv({
  FASTAPI_URL: process.env.FASTAPI_URL || "http://localhost:8000",
  SOLANA_RPC: process.env.SOLANA_RPC || "http://localhost:8899",
  PROGRAM_ID: process.env.PROGRAM_ID || "11111111111111111111111111111111",
});