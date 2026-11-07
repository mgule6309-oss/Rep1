// MongoDB Shell (mongosh) examples. These commands are illustrative and have NOT been run here.
use community_library

db.loans.insertOne({
  _id: "loan-2026-0002",
  member: { memberId: 2, name: "David Okafor", email: "david@example.test" },
  items: [{ copyId: 3, title: "The Joys of Motherhood", dueOn: ISODate("2026-11-03"), returnedOn: null }],
  eventHistory: [{ type: "LOAN_CREATED", at: ISODate("2026-10-20T10:30:00Z") }]
});

db.loans.createIndex({ "member.memberId": 1, "items.dueOn": 1 });
db.loans.find({ "member.memberId": 2, "items.returnedOn": null });
db.loans.aggregate([
  { $unwind: "$items" },
  { $match: { "items.returnedOn": null } },
  { $group: { _id: "$items.title", activeCount: { $sum: 1 } } },
  { $sort: { activeCount: -1 } }
]);
