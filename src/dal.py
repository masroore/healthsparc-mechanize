from . import db, enum_utils, utils


def procedures_catalog() -> list[dict]:
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


def lab_order_details(invoice_id: int) -> dict:
    sql = """
SELECT
	ord.InvoiceId AS invoice_id,
	ord.OrderId AS order_id,
	ord.RowGuid AS invoice_guid,
	ord.OrderDateTime AS order_datetime,
	ord.WorkflowStage AS workflow_stage,
	ord.LastModified AS updated_at,
	ord.IsCancelled AS is_canceled,
	IIF(inv.PaymentStatus = 30, 1, 0) AS paid_in_full,
	inv.GrossPayable AS gross_payable,
	inv.DiscountAmount AS discount_amount,
	inv.TaxAmount AS tax_amount,
	inv.SurchargeAmount AS surcharge_amount,
	inv.NetPayable AS net_payable,
	inv.PaidAmount AS paid_amount,
	inv.DueAmount AS due_amount,
	inv.RefundAmount AS refund_amount,
	ref.Id AS referrer_source_id,
	ref.RowGuid AS referrer_source_guid,
	ref.FullName AS referrer_full_name,
	ord.ReferrerCustomName AS referrer_custom_name,
	ord.DisallowReferral AS disallow_referral,
	ord.AssociateLabId AS associate_lab_source_id,
	assoc.RowGuid AS associate_lab_source_guid,
	ord.SubOrderTrackingId AS associate_lab_tracking_id,
	ord.IsExternalSubOrder AS is_outer_order,
	ord.RegisteredMemberId AS patient_upin,
	ord.Title AS patient_title,
	ord.FirstName AS patient_first_name,
	ord.LastName AS patient_last_name,
	ord.Sex AS patient_sex,
	CASE
        WHEN ord.Sex = 10 THEN 'M'
        WHEN ord.Sex = 20 THEN 'F'
        ELSE 'U'
    END AS patient_gender,
	ord.Age AS patient_age,
	ord.DoB AS patient_dob,
	ord.OrderNotes AS order_notes,
	ord.WebAccessToken AS access_token 
FROM
	PROE.PatientLabOrders AS ord
	INNER JOIN Finances.InvoiceMaster AS inv ON ord.InvoiceId = inv.InvoiceId
	LEFT JOIN [Catalog].Referrers AS ref ON ord.ReferrerId = ref.Id
	LEFT JOIN SubContract.AssociateLabs AS assoc ON ord.AssociateLabId = assoc.Id 
WHERE
	ord.InvoiceId = ?    
    """
    return db.fetch(sql, invoice_id)


def lab_order_result_bundles(invoice_id: int) -> list[dict]:
    sql = """
SELECT
	Id AS bundle_id,
	TestResultType AS bundle_type,
	WorkflowStage AS workflow_stage,
	DisplayTitle AS bundle_title,
	ComponentLabTests AS bundle_components,
	FinalizingConsultantName AS consultant_name,
	DateCreated AS created_at,
	LastUpdated AS updated_at 
FROM
	TestResults.ResultBundles 
WHERE
	IsActive = 1 
	AND InvoiceId = ?
	"""

    bundles = db.fetch_all(sql, invoice_id)
    for b in bundles:
        workflow_stage = int(b["workflow_stage"])
        bundle_type = int(b["bundle_type"])
        b["render_report"] = bundle_type != 0 and enum_utils.wf_can_generate_report(
            workflow_stage
        )
        b["workflow_stage_descr"] = enum_utils.wf_stage_descr(workflow_stage)
        b["bundle_type_descr"] = enum_utils.result_bundle_type(bundle_type)
        b["progress_pct"] = enum_utils.wf_progress_pct(workflow_stage)

    return bundles


def referrers_catalog() -> list[dict]:
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