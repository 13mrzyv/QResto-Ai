SCHEMA = """
Verilənlər bazası: QRestoDB (SQL Server)

Cədvəllər və sütunlar:

Categories: Id (int), Name (nvarchar), IsActive (bit: 1=Aktiv, 0=Deaktiv)

Products: Id (int), CategoryId (int), Name (nvarchar), Price (decimal), 
          Description (nvarchar), IsAvailable (bit: 1=Var, 0=Yoxdur), 
          ImageUrl (nvarchar), IsDeleted (bit: 1=Silinib, 0=Aktiv)

Tables: Id (int), TableNumber (nvarchar), Status (int: 0=Boş, 1=Dolu), QRToken (nvarchar)

Orders: Id (int), TableId (int), OrderDate (datetime), TotalAmount (decimal),
        Status (int: 1=Hazırlanır, 2=Ödənildi)

OrderItems: Id (int), OrderId (int), ProductId (int), Quantity (int), 
            UnitPrice (decimal), OrderDate (datetime), Note (nvarchar)

Expenses: Id (int), Description (nvarchar), Amount (decimal), ExpenseDate (datetime)

Əlaqələr:
- OrderItems.OrderId → Orders.Id
- OrderItems.ProductId → Products.Id
- Orders.TableId → Tables.Id
- Products.CategoryId → Categories.Id

Vacib qaydalar:
- Silinmiş məhsulları göstərmə: Products.IsDeleted = 0
- Aktiv məhsullar: Products.IsAvailable = 1
- Ödənilmiş sifarişlər: Orders.Status = 2
- Boş masalar: Tables.Status = 0, Dolu masalar: Tables.Status = 1
- Məhsul satış tarixini yoxlayarkən həmişə OrderItems.OrderDate istifadə et, Orders.OrderDate yox.
- Satış sayını hesablayarkən: SUM(OrderItems.Quantity)
- "Total" və ya "Quantity" sütunları ƏDƏD bildirir, pul deyil.
- Pul məbləği yalnız Price, UnitPrice, TotalAmount, Amount sütunlarında olur.
"""