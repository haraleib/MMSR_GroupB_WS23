import path from "node:path";
import { promises as fsPromises } from "node:fs";

interface Retrieval {
  [key: string]: [string, number][];
}

const getPath = (...filename: string[]) =>
  path.join(process.cwd(), "db", ...filename);

const getRetrievals = async () => {
  const dirPath = getPath("retrievals");
  const files = await fsPromises.readdir(dirPath);

  const map: Record<string, Retrieval> = {};
  try {
    for (const file of files) {
      const filePath = path.join(dirPath, file);
      const content = await fsPromises.readFile(filePath, "utf-8");
      map[file] = JSON.parse(content);
    }
  } catch (e) {
    console.error("getRetrievals(): ", e);
  }
  return map;
};

const getMetadata = async () => {
  const path = getPath("songMeta.json");
  const content = await fsPromises.readFile(path, "utf-8");
  return JSON.parse(content) as Song[];
};

export const metadata = await getMetadata();
export const retrievals = await getRetrievals();