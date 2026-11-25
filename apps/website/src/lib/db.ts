import { PrismaClient } from "@/generated/prisma/client";
import { PrismaPg } from "@prisma/adapter-pg";
import { Pool } from "pg";
import { getDatabaseUrl } from "@/lib/env";

function createPrismaClient() {
  const pool = new Pool({ connectionString: getDatabaseUrl() });
  const adapter = new PrismaPg(pool);
  return new PrismaClient({ adapter });
}

declare global {
  var prismaGlobal: PrismaClient | undefined;
}

let db: PrismaClient | undefined;

export function getDb(): PrismaClient {
  if (db) return db;
  db = globalThis.prismaGlobal ?? createPrismaClient();
  if (process.env.NODE_ENV !== "production") globalThis.prismaGlobal = db;
  return db;
}
