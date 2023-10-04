from datetime import datetime, timedelta

from . import db


def daily_sales_daterange(start_dt: datetime, end_dt: datetime):
    sql = """
SELECT
  CONVERT(DATE, PROE.PatientLabOrders.OrderDateTime) AS order_date
 ,COUNT(*) AS num_patients
 ,CAST(SUM(Finances.InvoiceMaster.GrossPayable) AS INTEGER) AS gross
 ,CAST(SUM(Finances.InvoiceMaster.DiscountAmount) AS INTEGER) AS discount
 ,CAST(SUM(Finances.InvoiceMaster.NetPayable) AS INTEGER) AS net
 ,CAST(SUM(Finances.InvoiceMaster.PaidAmount) AS INTEGER) AS paid
 ,CAST(SUM(Finances.InvoiceMaster.DueAmount) AS INTEGER) AS due
 ,0 AS referral
FROM PROE.PatientLabOrders
  INNER JOIN Finances.InvoiceMaster
  ON Finances.InvoiceMaster.InvoiceId = PROE.PatientLabOrders.InvoiceId
WHERE PROE.PatientLabOrders.IsCancelled = 0
AND CONVERT(DATE, PROE.PatientLabOrders.OrderDateTime) BETWEEN ? AND ?
GROUP BY CONVERT(DATE, PROE.PatientLabOrders.OrderDateTime)
ORDER BY CONVERT(DATE, PROE.PatientLabOrders.OrderDateTime)	     	
    """
    return db.fetch_all(sql, start_dt.strftime("%Y-%m-%d"), end_dt.strftime("%Y-%m-%d"))


def daily_sales_past_days(days: int = 30):
    end_dt = datetime.now()
    start_dt = end_dt - timedelta(days=days)
    return daily_sales_daterange(start_dt, end_dt)


def referrer_sales_date(dt: datetime):
    sql = """
SELECT
  PatientLabOrders.ReferrerId AS upin
 ,COUNT(*) AS num_patients
 ,CAST(SUM(Finances.InvoiceMaster.GrossPayable) AS INTEGER) AS gross
 ,CAST(SUM(Finances.InvoiceMaster.DiscountAmount) AS INTEGER) AS discount
 ,CAST(SUM(Finances.InvoiceMaster.NetPayable) AS INTEGER) AS net
 ,CAST(SUM(Finances.InvoiceMaster.PaidAmount) AS INTEGER) AS paid
 ,CAST(SUM(Finances.InvoiceMaster.DueAmount) AS INTEGER) AS due
 ,0 AS referral
FROM PROE.PatientLabOrders
INNER JOIN Finances.InvoiceMaster
  ON Finances.InvoiceMaster.InvoiceId = PROE.PatientLabOrders.InvoiceId
WHERE PROE.PatientLabOrders.IsCancelled = 0
AND PROE.PatientLabOrders.ReferrerId IS NOT NULL
AND CONVERT(DATE, PROE.PatientLabOrders.OrderDateTime) = ?
GROUP BY PROE.PatientLabOrders.ReferrerId	    
        """
    return db.fetch_all(sql, dt.strftime("%Y-%m-%d"))


def referrer_sales_daterange(start_dt: datetime, end_dt: datetime):
    sql = """
SELECT
  PatientLabOrders.ReferrerId AS upin
 ,COUNT(*) AS num_patients
 ,CAST(SUM(Finances.InvoiceMaster.GrossPayable) AS INTEGER) AS gross
 ,CAST(SUM(Finances.InvoiceMaster.DiscountAmount) AS INTEGER) AS discount
 ,CAST(SUM(Finances.InvoiceMaster.NetPayable) AS INTEGER) AS net
 ,CAST(SUM(Finances.InvoiceMaster.PaidAmount) AS INTEGER) AS paid
 ,CAST(SUM(Finances.InvoiceMaster.DueAmount) AS INTEGER) AS due
 ,0 AS referral
FROM PROE.PatientLabOrders
INNER JOIN Finances.InvoiceMaster
  ON Finances.InvoiceMaster.InvoiceId = PROE.PatientLabOrders.InvoiceId
WHERE PROE.PatientLabOrders.IsCancelled = 0
AND PROE.PatientLabOrders.ReferrerId IS NOT NULL
AND CONVERT(DATE, PROE.PatientLabOrders.OrderDateTime) BETWEEN ? AND ?
GROUP BY PROE.PatientLabOrders.ReferrerId    
    """
    return db.fetch_all(sql, start_dt.strftime("%Y-%m-%d"), end_dt.strftime("%Y-%m-%d"))
