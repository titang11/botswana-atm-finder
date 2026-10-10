 DATA QUALITY & VERIFICATION RULES

## Context & Purpose
The goal of ATM Finder Botswana is to provide users with trustworthy, reliable, and verified location data for ATMs across Botswana. Unreliable or hallucinated coordinates can stranded users searching for cash. 

All contributors, data engineers, and AI research agents operating on this repository must strictly adhere to the following 11 mandatory Data Quality Rules.

---

## Data Quality Rules & Constraints

### 1. Absolute Prohibition of Fabrication
Never invent, estimate, or hallucinate an ATM location, bank name, street address, supported service, GPS coordinate, or operating status. If data cannot be confirmed from an official published source, it must be marked as missing (`null` or `unknown`).

### 2. Mandatory Source Lineage
Every ATM record must retain the original `source_url` from which the location was discovered (e.g., official bank directories, published locators). Unreferenced data is strictly forbidden.

### 3. Null Coordinate Protocol
If exact, pin-level GPS coordinates cannot be verified:
- Set `latitude` to `null`.
- Set `longitude` to `null`.
- Preserve the official published address string.
- Flag the record as `published_unverified` or `address_to_confirm`.
- *Do not attempt to guess or place approximate town-level center coordinates.*

### 4. Operational Status Standards
Set `operational_status` to `"unknown"` by default unless active physical evidence or an official bank operational feed confirms the machine is operational (`"operational"`) or out of service (`"out_of_service"`).

### 5. Verification Status Lifecycle
Every record must use one of three explicit status values:
- `published_unverified`: Discovered in an official published bank directory, but not independently verified on the ground.
- `address_to_confirm`: The official address provided is ambiguous or lacks landmark precision (e.g., "Main Mall Branch").
- `verified`: Physical location and exact GPS pin independently confirmed via satellite, field verification, or official map parameter extraction.

### 6. Verification Tracking
Whenever a record is updated or verified, update the `last_verified` date (format `YYYY-MM-DD`) and record the verification method in the `notes` field.

### 7. Unit Preservation (Multi-ATM Sites)
When an official source explicitly lists separate ATM units at a single venue (e.g., "Airport Junction ATM 1" and "Airport Junction ATM 2"), preserve them as separate records. Do not merge separate machines into a single entry.

### 8. Granular Service Identification
Explicitly list supported services in the `services` array:
- `cash_withdrawal`
- `deposit`
- `foreign_currency_zar` / `foreign_currency_usd`
Do not assume every machine supports all functions (such as cash deposits or forex).

### 9. Conflict Resolution Protocol
If two official sources conflict regarding an ATM’s location, services, or status:
- Document the discrepancy clearly in the `notes` field.
- Keep the operational/verification status as `published_unverified` or `address_to_confirm`.
- Do not silently pick an arbitrary answer.

### 10. Honest Coverage Claims
Never state or imply that the database covers 100% of ATMs in Botswana unless full national coverage has been systematically proven and audited.

### 11. Distance-Based Ranking Exclusion
In the web application, ATMs with `null` coordinates must be excluded from distance-based distance calculations (Haversine formula), but must remain searchable by town, bank, and landmark text search.
