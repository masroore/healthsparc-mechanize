from datetime import datetime, timedelta

from . import db, utils


def daily_sales_daterange(
    branch_uid: str, start_dt: datetime, end_dt: datetime
) -> list[dict]:
    sql = """
SELECT
	'%s' AS branch_uid,
	CONVERT ( DATE, PROE.PatientLabOrders.OrderDateTime ) AS order_date,
	COUNT ( * ) AS num_patients,
	CAST ( SUM ( Finances.InvoiceMaster.GrossPayable ) AS INTEGER ) AS gross_payable,
	CAST ( SUM ( Finances.InvoiceMaster.DiscountAmount ) AS INTEGER ) AS discount_amount,
	CAST ( SUM ( Finances.InvoiceMaster.NetPayable ) AS INTEGER ) AS net_payable,
	CAST ( SUM ( Finances.InvoiceMaster.PaidAmount ) AS INTEGER ) AS paid_amount,
	CAST ( SUM ( Finances.InvoiceMaster.DueAmount ) AS INTEGER ) AS due_amount,
	0 AS referral_amount 
FROM
	PROE.PatientLabOrders
	INNER JOIN Finances.InvoiceMaster ON Finances.InvoiceMaster.InvoiceId = PROE.PatientLabOrders.InvoiceId 
WHERE
	PROE.PatientLabOrders.IsCancelled = 0 
	AND CONVERT ( DATE, PROE.PatientLabOrders.OrderDateTime ) BETWEEN ? AND ? 
GROUP BY
	CONVERT ( DATE, PROE.PatientLabOrders.OrderDateTime ) 
ORDER BY
	CONVERT ( DATE, PROE.PatientLabOrders.OrderDateTime )
    """
    rows = db.fetch_all(sql % branch_uid, utils.dt_str(start_dt), utils.dt_str(end_dt))
    for r in rows:
        r["order_date"] = utils.dt_str(r["order_date"])
    return rows


def daily_sales_past_days(branch_uid: str, days: int = 30) -> list[dict]:
    end_dt = datetime.now()
    start_dt = end_dt - timedelta(days=days)
    return daily_sales_daterange(branch_uid, start_dt, end_dt)


def referrer_sales_by_date(branch_uid: str, dt: datetime) -> list[dict]:
    sql = """
SELECT
    '%s' AS branch_uid,
	Referrers.Id AS referrer_id,
	Referrers.RowGuid AS referrer_guid,
	-- referrer_upin
	COUNT ( * ) AS num_patients,
	CAST ( SUM ( Finances.InvoiceMaster.GrossPayable ) AS INTEGER ) AS gross_payable,
	CAST ( SUM ( Finances.InvoiceMaster.DiscountAmount ) AS INTEGER ) AS discount_amount,
	CAST ( SUM ( Finances.InvoiceMaster.NetPayable ) AS INTEGER ) AS net_payable,
	CAST ( SUM ( Finances.InvoiceMaster.PaidAmount ) AS INTEGER ) AS paid_amount,
	CAST ( SUM ( Finances.InvoiceMaster.DueAmount ) AS INTEGER ) AS due_amount,
	0 AS referral_amount 
FROM
	PROE.PatientLabOrders
	INNER JOIN Finances.InvoiceMaster ON Finances.InvoiceMaster.InvoiceId = PROE.PatientLabOrders.InvoiceId
	INNER JOIN [Catalog].Referrers ON PROE.PatientLabOrders.ReferrerId = [Catalog].Referrers.Id 
WHERE
	PROE.PatientLabOrders.IsCancelled = 0 
	AND PROE.PatientLabOrders.ReferrerId IS NOT NULL 
	AND CONVERT ( DATE, PROE.PatientLabOrders.OrderDateTime ) = ?
GROUP BY
	Referrers.Id,
	Referrers.RowGuid	    
        """
    return db.fetch_all(sql % branch_uid, utils.dt_str(dt))


def referrer_sales_daterange(
    branch_uid: str, start_dt: datetime, end_dt: datetime
) -> list[dict]:
    sql = """
SELECT
    '%s' AS branch_uid,
	Referrers.Id AS referrer_id,
	Referrers.RowGuid AS referrer_guid,
	-- referrer_upin
	COUNT ( * ) AS num_patients,
	CAST ( SUM ( Finances.InvoiceMaster.GrossPayable ) AS INTEGER ) AS gross_payable,
	CAST ( SUM ( Finances.InvoiceMaster.DiscountAmount ) AS INTEGER ) AS discount_amount,
	CAST ( SUM ( Finances.InvoiceMaster.NetPayable ) AS INTEGER ) AS net_payable,
	CAST ( SUM ( Finances.InvoiceMaster.PaidAmount ) AS INTEGER ) AS paid_amount,
	CAST ( SUM ( Finances.InvoiceMaster.DueAmount ) AS INTEGER ) AS due_amount,
	0 AS referral_amount 
FROM
	PROE.PatientLabOrders
	INNER JOIN Finances.InvoiceMaster ON Finances.InvoiceMaster.InvoiceId = PROE.PatientLabOrders.InvoiceId
	INNER JOIN [Catalog].Referrers ON PROE.PatientLabOrders.ReferrerId = [Catalog].Referrers.Id 
WHERE
	PROE.PatientLabOrders.IsCancelled = 0 
	AND PROE.PatientLabOrders.ReferrerId IS NOT NULL 
	AND CONVERT(DATE, PROE.PatientLabOrders.OrderDateTime) BETWEEN ? AND ? 
GROUP BY
	Referrers.Id,
	Referrers.RowGuid    
    """
    return db.fetch_all(sql % branch_uid, utils.dt_str(start_dt), utils.dt_str(end_dt))
