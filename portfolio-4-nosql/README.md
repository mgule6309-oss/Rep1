# Portfolio 4 — NoSQL document model

The sample document embeds a member snapshot, loan items and event history in one loan document. This is suitable for read patterns that usually retrieve a loan and its timeline together. It also allows event records to gain optional attributes without altering a fixed relational schema.

Trade-offs: embedded member data duplicates relational data and can become stale; large unbounded event arrays can grow excessively; cross-document consistency and stock control are harder. The relational database remains the authoritative source for copy availability and lending transactions. `mongosh` commands are examples only: no MongoDB server was available during this preparation, so no MongoDB execution is claimed.
