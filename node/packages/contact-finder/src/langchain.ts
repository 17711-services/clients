/**
 * LangChain.js tools for 📇 contact-finder-service, grouped in one Toolkit -- one tool per operation, each just an async function (JS has no separate sync form to generate). Requires the `@langchain/core`+`zod` peer dependencies declared in this package's own package.json -- imported from `contact-finder/langchain`, never from the package root, so importing the base client never requires them installed.
 */

import { tool } from "@langchain/core/tools";
import { z } from "zod";
import { Client } from "./index.js";

export class ContactFinderToolkit {
  private client: Client;

  constructor(client: Client) {
    this.client = client;
  }

  getTools() {
    return [
      tool(
        async (input) => this.client.getContacts(input),
        {
          name: "getContacts",
          description: "Contact finder: public business emails, phone numbers, contact forms and support pages of a domain, with role and source ($0.009, x402)",
          schema: z.object({ company_name: z.string().nullable().optional(), domain: z.string().nullable().optional(), max_age_seconds: z.number().nullable().optional() }),
        },
      ),
    ];
  }
}
