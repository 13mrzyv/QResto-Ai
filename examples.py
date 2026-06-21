EXAMPLES = """
Kontekst qaydası:
Əgər sual qısa və natamamdırsa (məsələn "bəs X?"), bu əvvəlki sualın davamıdır.
Yalnız ƏN SON sual-cavab cütünün strukturunu götür, ondan əvvəlkiləri nəzərə alma.

Nümunə 1:
Sual: Bugün neçə latte satılıb?
SQL: SELECT P.Name, SUM(OI.Quantity) as Total FROM OrderItems OI JOIN Products P ON OI.ProductId = P.Id WHERE P.Name LIKE '%latte%' AND CAST(OI.OrderDate AS DATE) = CAST(GETDATE() AS DATE) GROUP BY P.Name

Nümunə 2:
Sual: Bu ay ən çox satılan məhsul hansıdır?
SQL: SELECT TOP 1 P.Name, SUM(OI.Quantity) as Total FROM OrderItems OI JOIN Products P ON OI.ProductId = P.Id JOIN Orders O ON OI.OrderId = O.Id WHERE MONTH(O.OrderDate) = MONTH(GETDATE()) AND YEAR(O.OrderDate) = YEAR(GETDATE()) GROUP BY P.Name ORDER BY Total DESC

Nümunə 3:
Sual: Bugünkü ümumi gəlir nə qədərdir?
SQL: SELECT SUM(TotalAmount) as UmumiGelir FROM Orders WHERE CAST(OrderDate AS DATE) = CAST(GETDATE() AS DATE) AND Status = 2

Nümunə 4:
Sual: Hal hazırda neçə masa doludur?
SQL: SELECT COUNT(*) as DoluMasalar FROM Tables WHERE Status = 1

Nümunə 5:
Sual: Bu həftə ən çox satılan 5 məhsul hansılardır?
SQL: SELECT TOP 5 P.Name, SUM(OI.Quantity) as Total FROM OrderItems OI JOIN Products P ON OI.ProductId = P.Id JOIN Orders O ON OI.OrderId = O.Id WHERE O.OrderDate >= DATEADD(DAY, -7, GETDATE()) GROUP BY P.Name ORDER BY Total DESC

Nümunə 6:
Sual: Bugünkü xərclər nə qədərdir?
SQL: SELECT SUM(Amount) as UmumiXerc FROM Expenses WHERE CAST(ExpenseDate AS DATE) = CAST(GETDATE() AS DATE)

Nümunə 7:
Sual: Ən bahalı məhsul hansıdır?
SQL: SELECT TOP 1 Name, Price FROM Products WHERE IsDeleted = 0 ORDER BY Price DESC

Nümunə 8:
Sual: Bu ay neçə sifariş olub?
SQL: SELECT COUNT(*) as Sifarisler FROM Orders WHERE MONTH(OrderDate) = MONTH(GETDATE()) AND YEAR(OrderDate) = YEAR(GETDATE())

Nümunə 9 (çox sözlü məhsul adı):
Sual: Bugün San Sebastian neçə ədəd satılıb?
SQL: SELECT P.Name, SUM(OI.Quantity) as Total FROM OrderItems OI JOIN Products P ON OI.ProductId = P.Id WHERE P.Name LIKE '%San Sebastian%' AND CAST(OI.OrderDate AS DATE) = CAST(GETDATE() AS DATE) GROUP BY P.Name

Nümunə 10 (kontekstli sual):
Əvvəlki sual: Ən çox espresso sifariş verən masa hansıdır?
İndiki sual: bəs Latte?
Bu sualın həqiqi mənası: Ən çox latte sifariş verən masa hansıdır?
SQL: SELECT TOP 1 T.TableNumber, SUM(OI.Quantity) as Total FROM OrderItems OI JOIN Products P ON OI.ProductId = P.Id JOIN Orders O ON OI.OrderId = O.Id JOIN Tables T ON O.TableId = T.Id WHERE P.Name LIKE '%latte%' GROUP BY T.TableNumber ORDER BY Total DESC

Nümunə 11 (zaman aralığı):
Sual: Son 10 gündə ən çox satılan məhsul hansıdır?
SQL: SELECT TOP 1 P.Name, SUM(OI.Quantity) as Total FROM OrderItems OI JOIN Products P ON OI.ProductId = P.Id WHERE OI.OrderDate >= DATEADD(DAY, -10, GETDATE()) GROUP BY P.Name ORDER BY Total DESC
"""

NUMUNELER_LIST = [
    {
        "sual": "Bugün neçə latte satılıb?",
        "sql": "SELECT SUM(OI.Quantity) as Total FROM OrderItems OI JOIN Products P ON OI.ProductId = P.Id WHERE P.Name LIKE '%latte%' AND CAST(OI.OrderDate AS DATE) = CAST(GETDATE() AS DATE)"
    },
    {
        "sual": "Bu ay ən çox satılan məhsul hansıdır?",
        "sql": "SELECT TOP 1 P.Name, SUM(OI.Quantity) as Total FROM OrderItems OI JOIN Products P ON OI.ProductId = P.Id WHERE MONTH(OI.OrderDate) = MONTH(GETDATE()) AND YEAR(OI.OrderDate) = YEAR(GETDATE()) GROUP BY P.Name ORDER BY Total DESC"
    },
    {
        "sual": "Bugünkü ümumi gəlir nə qədərdir?",
        "sql": "SELECT SUM(TotalAmount) as UmumiGelir FROM Orders WHERE CAST(OrderDate AS DATE) = CAST(GETDATE() AS DATE) AND Status = 2"
    },
    {
        "sual": "Hal hazırda neçə masa doludur?",
        "sql": "SELECT COUNT(*) as DoluMasalar FROM Tables WHERE Status = 1"
    },
    {
        "sual": "Bu həftə ən çox satılan 5 məhsul hansılardır?",
        "sql": "SELECT TOP 5 P.Name, SUM(OI.Quantity) as Total FROM OrderItems OI JOIN Products P ON OI.ProductId = P.Id WHERE OI.OrderDate >= DATEADD(DAY, -7, GETDATE()) GROUP BY P.Name ORDER BY Total DESC"
    },
    {
        "sual": "Bugünkü xərclər nə qədərdir?",
        "sql": "SELECT SUM(Amount) as UmumiXerc FROM Expenses WHERE CAST(ExpenseDate AS DATE) = CAST(GETDATE() AS DATE)"
    },
    {
        "sual": "Ən bahalı məhsul hansıdır?",
        "sql": "SELECT TOP 1 Name, Price FROM Products WHERE IsDeleted = 0 ORDER BY Price DESC"
    },
    {
        "sual": "Bu ay neçə sifariş olub?",
        "sql": "SELECT COUNT(*) as Sifarisler FROM Orders WHERE MONTH(OrderDate) = MONTH(GETDATE()) AND YEAR(OrderDate) = YEAR(GETDATE())"
    },
    {
        "sual": "Bugün San Sebastian neçə ədəd satılıb?",
        "sql": "SELECT P.Name, SUM(OI.Quantity) as Total FROM OrderItems OI JOIN Products P ON OI.ProductId = P.Id WHERE P.Name LIKE '%San Sebastian%' AND CAST(OI.OrderDate AS DATE) = CAST(GETDATE() AS DATE) GROUP BY P.Name"
    },
    {
        "sual": "Latte neçə fərqli masada sifariş edilib?",
        "sql": "SELECT COUNT(DISTINCT O.TableId) as Total FROM OrderItems OI JOIN Products P ON OI.ProductId = P.Id JOIN Orders O ON OI.OrderId = O.Id WHERE P.Name LIKE '%latte%'"
    },
]