from src import db, utils


def get_procedures() -> list[dict]:
    sql = """
SELECT
	[Catalog].LabTests.Id AS procedure_id,
	[Catalog].LabTests.TestSKU AS procedure_sku,
	[Catalog].LabTests.CanonicalName AS procedure_name,
	[Catalog].LabTests.ListPrice AS procedure_price,
	[Catalog].LabTests.RowGuid AS procedure_guid,
	[Catalog].Labs.Id AS category_id,
	[Catalog].Labs.LabCode AS category_code,
	[Catalog].Labs.CategoryName AS category_name,
	[Catalog].Labs.RowGuid AS category_guid,
	[Catalog].DiscountLevels.DiscountMode AS discount_mode,
	[Catalog].DiscountLevels.DiscountPercent AS discount_percent,
	[Catalog].DiscountLevels.DiscountAmount AS discount_amount,
	[Catalog].DiscountLevels.RowGuid AS discount_guid 
FROM
	[Catalog].LabTests
	INNER JOIN [Catalog].Labs ON [Catalog].LabTests.PerformingLabId = [Catalog].Labs.Id
	LEFT JOIN [Catalog].DiscountLevels ON [Catalog].Labs.DiscountLevelId = [Catalog].DiscountLevels.Id 
WHERE
	[Catalog].LabTests.IsActive = 1 
	AND [Catalog].Labs.IsActive = 1 
	AND [Catalog].Labs.IsAuxProcedure = 0 
ORDER BY
	category_id ASC,
	procedure_name ASC
    """
    return db.fetch_all(sql)


def get_referrers() -> list[dict]:
    sql = """
SELECT
	Id AS source_id,
	RowGuid AS source_guid,
	FullName AS name,
	Name AS name_only,
	IdentifyingTag AS tag,
	MobilePhone AS phone,
	SuppressNetReferral AS disallow_referral,
	WebLoginEnabled AS web_access,
	WebLoginId AS username,
	WebPassKey AS password,
	LastUpdated AS updated_at 
FROM
	[Catalog].Referrers    
    """
    refs = db.fetch_all(sql)
    for r in refs:
        r["upin"] = utils.hashify([r["name"], r["tag"], r["phone"]])
        r["initials"] = utils.initials(r["name_only"])

    return refs


def report_pdf(bundle_id: int):
    pass
