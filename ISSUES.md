# Issues Analysis

## Summary

| Type | Critical | High | Medium | Low | Total |
|------|----------|------|--------|-----|-------|
| Product Issues | 0 | 1 | 2 | 0 | 3 |
| Code Issues | 0 | 2 | 1 | 0 | 3 |

---

## Product Issues

### [P1] Test Case Data Is Truncated During Database Migration

**Severity**: High

**Location**: `problems/views.py` – `migrate_test_cases_to_db` section

**Description**:

During database migration, the input and output of each test case are limited to the first 260 characters.

**Impact**:
- Large test cases lose important input and expected output data.
- Users cannot retrieve the complete test cases from the database.
- Test-case information may become incorrect or unusable.

**Suggested Fix**:

Store complete test-case data without truncation, or use Azure Blob Storage as the source of truth for full test-case files.

---

### [P2] Old Test Cases Remain After Re-Migration

**Severity**: Medium

**Location**: `problems/views.py` – `migrate_test_cases_to_db` section

**Description**:

When existing test cases are updated, the code updates or creates records but does not delete extra records that are no longer present in Polygon.

**Impact**:
- Outdated test cases remain in the database.
- The database may contain more test cases than the current Polygon problem.
- Users may access incorrect or outdated test-case information.

**Suggested Fix**:

After migration, compare the existing records with the latest Polygon test cases and delete obsolete records.

---

### [P3] No Confirmation Before Replacing Azure Test Cases

**Severity**: Medium

**Location**: `problems/polygon_api.py` – `migrate_to_azure_blob`

**Description**:

The migration function deletes the existing test-case blobs before uploading the new test cases. There is no separate confirmation step before replacing the existing data.

**Impact**:
- An accidental migration can remove existing test-case files.
- If the upload fails after deletion, the previous data may no longer be available.
- Users may experience incomplete test-case storage.

**Suggested Fix**:

Add a confirmation step and use a safer replacement strategy, such as uploading to a temporary location and switching only after successful verification.

---

## Code Issues

### [C1] Test Case Data Is Hard-Coded to 260 Characters

**Severity**: High

**Location**: `problems/views.py` – database test-case migration logic

**Description**:

The code explicitly truncates input and output:

```python
truncated_input = input_data[:260]
truncated_output = output_data[:260]
```

This causes data loss for test cases longer than 260 characters.

**Impact**:
- Complete test-case information is not preserved.
- Large test cases cannot be reconstructed from the database.
- Data integrity is affected.

**Suggested Fix**:

Remove the truncation and use suitable storage fields or external file storage for large test-case data.

---

### [C2] Missing Cleanup of Obsolete Database Records

**Severity**: High

**Location**: `problems/views.py` – `migrate_test_cases_to_db` section

**Description**:

The migration code retrieves existing test cases and updates them by index. It creates new records when required but does not remove records left over when the latest Polygon test-case count is smaller.

**Impact**:
- Duplicate or outdated records may remain.
- Database records become inconsistent with Polygon.
- Future migrations may operate on incorrect data.

**Suggested Fix**:

Use a transaction to synchronize the database with the latest test-case collection. Remove obsolete records after successful synchronization.

---

### [C3] Azure Upload Is Not Transactionally Safe

**Severity**: Medium

**Location**: `problems/polygon_api.py` – `migrate_to_azure_blob`

**Description**:

The migration deletes existing Azure blobs before uploading new test cases. Database transactions cannot automatically roll back changes made to Azure Blob Storage.

The view contains a compensating cleanup attempt, but the deletion logic is not fully implemented.

**Impact**:
- A failed upload can leave Azure with incomplete data.
- Previous test-case files may be lost.
- Database rollback does not restore deleted Azure blobs.

**Suggested Fix**:

Use a temporary blob prefix, upload all files, verify them, and then replace the previous data. Implement reliable rollback or recovery handling.

---

## Edge Case Analysis

### Q1

**A Polygon problem has 0 sample test cases but 15 regular test cases. What happens when you migrate this problem?**

The application separates sample test cases from regular test cases.

- The sample-test migration loop finds no sample cases, so no sample records are created or updated.
- The regular test-case migration processes all 15 cases through `ProblemTestCase`.
- Azure migration also processes the regular test cases, provided each has both input and output.

Therefore, the regular test cases can still be migrated even when there are no sample test cases.

---

### Q2

**A problem is migrated with 20 test cases. Later, the problem setter removes 8 test cases on Polygon (now 12 remain). The problem is re-migrated. What happens?**

During database migration:

- The first 12 existing records are updated.
- The code does not delete the remaining 8 old records.
- Therefore, 8 outdated test-case records remain in the database.

During Azure migration, the existing test-case blobs are deleted first, and the new test cases are uploaded. If the upload completes successfully, Azure contains the new 12 cases.

---

### Q3

**Two different Polygon problems have the exact same title: "Two Sum". You migrate the first one successfully. Then you try to migrate the second one. What happens?**

The database migration searches for an existing problem using its Polygon ID, not its title.

Therefore, the second problem is treated as a separate problem because it has a different Polygon ID.

Both problems may have the same title and generated slug. If the database enforces slug uniqueness, the second migration may fail with a database integrity error. Otherwise, both records can be stored with the same slug.

A better solution is to generate unique slugs and maintain Polygon ID as the unique external identifier.

---

### Q4

**When test cases are saved to the database via "Migrate Test Cases to DB", some data is intentionally discarded. What data is lost? Why might this cause problems?**

The migration intentionally truncates input and output data to the first 260 characters.

```python
truncated_input = input_data[:260]
truncated_output = output_data[:260]
```

This means all characters after the first 260 are discarded.

This can cause problems because:
- Large test cases become incomplete.
- Important input values may be lost.
- Expected output may be incorrect or incomplete.
- Test cases stored in the database cannot accurately represent the original Polygon data.

The full test-case files should be preserved in Azure Blob Storage.

---

## Notes

The application uses Django to manage problem metadata and test-case records, Polygon API to retrieve problem information, Redis to cache test cases, and Azure Blob Storage to store full test-case files.

The migration workflow would benefit from stronger data synchronization, post-upload verification, and safer handling of Azure storage failures.

Problem 69933 is interactive and requires a separate interactor-based execution system. A normal input/output comparison is not sufficient to judge interactive solutions.