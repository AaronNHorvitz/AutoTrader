import json 

exog_symbols_data = [

    # Commodities (~Futures ~Energy)
    {
        "Symbol": "CL=F",
        "Title": "WTI Crude Oil",
        "Explanation of what this": "Futures price of West Texas Intermediate crude oil.",
        "Explanation of why it may be important": "Influences energy stocks (e.g., XOM) and inflation expectations, leading market moves.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "BZ=F",
        "Title": "Brent Crude Oil",
        "Explanation of what this": "Futures price of Brent crude oil.",
        "Explanation of why it may be important": "Global oil benchmark, impacts energy stocks and economic activity signals.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "NG=F",
        "Title": "Natural Gas",
        "Explanation of what this": "Futures price of natural gas.",
        "Explanation of why it may be important": "Affects utility and energy stocks, reflects industrial demand.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "HO=F",
        "Title": "Heating Oil",
        "Explanation of what this": "Futures price of heating oil.",
        "Explanation of why it may be important": "Influences energy sector and consumer spending patterns.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "RB=F",
        "Title": "Gasoline",
        "Explanation of what this": "Futures price of RBOB gasoline.",
        "Explanation of why it may be important": "Drives energy costs, impacts consumer and transport stocks.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    
    # Commodities (~Futures ~Precious/Industrial Metals)
    {
        "Symbol": "GC=F",
        "Title": "Gold",
        "Explanation of what this": "Futures price of gold.",
        "Explanation of why it may be important": "Safe-haven asset, signals risk-off moves affecting equity markets.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "SI=F",
        "Title": "Silver",
        "Explanation of what this": "Futures price of silver.",
        "Explanation of why it may be important": "Industrial and safe-haven demand, impacts mining and tech stocks.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-10 days"
    },
    {
        "Symbol": "PL=F",
        "Title": "Platinum",
        "Explanation of what this": "Futures price of platinum.",
        "Explanation of why it may be important": "Industrial use (e.g., autos), leads manufacturing stocks.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "PA=F",
        "Title": "Palladium",
        "Explanation of what this": "Futures price of palladium.",
        "Explanation of why it may be important": "Key for auto catalysts, predicts auto sector performance.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "HG=F",
        "Title": "Copper",
        "Explanation of what this": "Futures price of copper.",
        "Explanation of why it may be important": "Economic growth indicator, leads industrial and construction stocks.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    
    # Commodities (~Futures ~Agriculture/Softs)
    {
        "Symbol": "ZC=F",
        "Title": "Corn",
        "Explanation of what this": "Futures price of corn.",
        "Explanation of why it may be important": "Affects food production costs, leads agriculture and consumer stocks.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "ZS=F",
        "Title": "Soybeans",
        "Explanation of what this": "Futures price of soybeans.",
        "Explanation of why it may be important": "Impacts food supply chains, predicts food stock performance.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "ZW=F",
        "Title": "Wheat",
        "Explanation of what this": "Futures price of wheat.",
        "Explanation of why it may be important": "Influences food prices, affects consumer and agriculture stocks.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "KC=F",
        "Title": "Coffee",
        "Explanation of what this": "Futures price of coffee.",
        "Explanation of why it may be important": "Reflects consumer discretionary trends, impacts retail stocks.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "SB=F",
        "Title": "Sugar",
        "Explanation of what this": "Futures price of sugar.",
        "Explanation of why it may be important": "Affects food production costs, leads consumer goods stocks.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "BAL=F",
        "Title": "Cotton",
        "Explanation of what this": "Futures price of cotton.",
        "Explanation of why it may be important": "Key input for apparel, predicts textile and retail stock moves.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "OJ=F",
        "Title": "Orange Juice",
        "Explanation of what this": "Futures price of orange juice.",
        "Explanation of why it may be important": "Reflects agricultural supply, impacts food and beverage stocks.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "LE=F",
        "Title": "Live Cattle",
        "Explanation of what this": "Futures price of live cattle.",
        "Explanation of why it may be important": "Affects meat production costs, leads food stock performance.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "HE=F",
        "Title": "Lean Hogs",
        "Explanation of what this": "Futures price of lean hogs.",
        "Explanation of why it may be important": "Influences meat supply chains, predicts food stock trends.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "LB=F",
        "Title": "Lumber",
        "Explanation of what this": "Futures price of lumber.",
        "Explanation of why it may be important": "Key for housing construction, leads real estate and industrial stocks.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    
    # Commodities (~ETFs ~Broad/Proxies)
    {
        "Symbol": "LIT",
        "Title": "Lithium & Battery Tech ETF",
        "Explanation of what this": "ETF tracking lithium and battery technology companies.",
        "Explanation of why it may be important": "Reflects EV and tech demand, leads related stocks (e.g., TSLA).",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "DBC",
        "Title": "Broad Commodity ETF",
        "Explanation of what this": "ETF tracking a broad commodity index.",
        "Explanation of why it may be important": "Broad economic activity signal, impacts multiple sectors.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "GLD",
        "Title": "Gold ETF",
        "Explanation of what this": "ETF tracking gold prices.",
        "Explanation of why it may be important": "Safe-haven proxy, signals risk-off moves affecting equities.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "SLV",
        "Title": "Silver ETF",
        "Explanation of what this": "ETF tracking silver prices.",
        "Explanation of why it may be important": "Industrial and safe-haven signal, impacts tech and mining stocks.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-10 days"
    },
    {
        "Symbol": "USO",
        "Title": "US Oil ETF",
        "Explanation of what this": "ETF tracking oil prices.",
        "Explanation of why it may be important": "Energy cost indicator, leads energy and transport stocks.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "UNG",
        "Title": "Natural Gas ETF",
        "Explanation of what this": "ETF tracking natural gas prices.",
        "Explanation of why it may be important": "Utility and industrial demand signal, impacts energy stocks.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "WOOD",
        "Title": "Timber & Forestry ETF",
        "Explanation of what this": "ETF tracking timber and forestry companies.",
        "Explanation of why it may be important": "Housing and construction proxy, leads related stocks.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "URA",
        "Title": "Uranium ETF",
        "Explanation of what this": "ETF tracking uranium companies.",
        "Explanation of why it may be important": "Energy transition signal, impacts utility and mining stocks.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "PALL",
        "Title": "Palladium ETF",
        "Explanation of what this": "ETF tracking palladium prices.",
        "Explanation of why it may be important": "Auto sector indicator, leads automotive stocks.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "PPLT",
        "Title": "Platinum ETF",
        "Explanation of what this": "ETF tracking platinum prices.",
        "Explanation of why it may be important": "Industrial demand signal, predicts manufacturing stocks.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    
    # Currencies (~Forex Major Pairs ~USD Base)
    {
        "Symbol": "EURUSD=X",
        "Title": "Euro/USD",
        "Explanation of what this": "Exchange rate between Euro and U.S. Dollar.",
        "Explanation of why it may be important": "Global trade signal, impacts multinational stocks (e.g., KO).",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "GBPUSD=X",
        "Title": "Pound/USD",
        "Explanation of what this": "Exchange rate between British Pound and U.S. Dollar.",
        "Explanation of why it may be important": "UK economic signal, affects U.S.-exposed stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "USDJPY=X",
        "Title": "USD/Japanese Yen",
        "Explanation of what this": "Exchange rate between U.S. Dollar and Japanese Yen.",
        "Explanation of why it may be important": "Yen carry trade signal, impacts global risk appetite.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "USDCNY=X",
        "Title": "USD/Chinese Yuan",
        "Explanation of what this": "Exchange rate between U.S. Dollar and Chinese Yuan.",
        "Explanation of why it may be important": "China trade signal, affects emerging market stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "USDCHF=X",
        "Title": "USD/Swiss Franc",
        "Explanation of what this": "Exchange rate between U.S. Dollar and Swiss Franc.",
        "Explanation of why it may be important": "Safe-haven currency, signals risk-off moves.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "USDCAD=X",
        "Title": "USD/Canadian Dollar",
        "Explanation of what this": "Exchange rate between U.S. Dollar and Canadian Dollar.",
        "Explanation of why it may be important": "Commodity currency, impacts energy and resource stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "AUDUSD=X",
        "Title": "Australian Dollar/USD",
        "Explanation of what this": "Exchange rate between Australian Dollar and U.S. Dollar.",
        "Explanation of why it may be important": "Commodity and China proxy, affects resource stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "NZDUSD=X",
        "Title": "New Zealand Dollar/USD",
        "Explanation of what this": "Exchange rate between New Zealand Dollar and U.S. Dollar.",
        "Explanation of why it may be important": "Commodity currency, signals global trade trends.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    
    # Currencies (~Forex ~More Majors + Crosses)
    {
        "Symbol": "XAUUSD=X",
        "Title": "Gold/USD Spot Price",
        "Explanation of what this": "Spot exchange rate of gold to U.S. Dollar.",
        "Explanation of why it may be important": "Safe-haven signal, leads risk-off equity moves.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "XAGUSD=X",
        "Title": "Silver/USD Spot Price",
        "Explanation of what this": "Spot exchange rate of silver to U.S. Dollar.",
        "Explanation of why it may be important": "Industrial demand signal, impacts mining and tech stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-10 days"
    },
    {
        "Symbol": "EURGBP=X",
        "Title": "Euro/Pound",
        "Explanation of what this": "Exchange rate between Euro and British Pound.",
        "Explanation of why it may be important": "European trade signal, affects UK and EU-exposed stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "AUDNZD=X",
        "Title": "Australian/New Zealand Dollar",
        "Explanation of what this": "Exchange rate between Australian and New Zealand Dollar.",
        "Explanation of why it may be important": "Commodity currency cross, signals regional trade trends.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "EURJPY=X",
        "Title": "Euro/Japanese Yen",
        "Explanation of what this": "Exchange rate between Euro and Japanese Yen.",
        "Explanation of why it may be important": "Risk appetite signal, impacts global equity trends.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "GBPJPY=X",
        "Title": "Pound/Japanese Yen",
        "Explanation of what this": "Exchange rate between British Pound and Japanese Yen.",
        "Explanation of why it may be important": "Carry trade signal, predicts risk-on/off moves.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "AUDJPY=X",
        "Title": "Australian Dollar/Japanese Yen",
        "Explanation of what this": "Exchange rate between Australian Dollar and Japanese Yen.",
        "Explanation of why it may be important": "Commodity and risk signal, impacts resource stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "NZDJPY=X",
        "Title": "New Zealand Dollar/Japanese Yen",
        "Explanation of what this": "Exchange rate between New Zealand Dollar and Japanese Yen.",
        "Explanation of why it may be important": "Commodity and risk signal, affects trade-exposed stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "EURCHF=X",
        "Title": "Euro/Swiss Franc",
        "Explanation of what this": "Exchange rate between Euro and Swiss Franc.",
        "Explanation of why it may be important": "Safe-haven cross, signals European risk sentiment.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "GBPCHF=X",
        "Title": "Pound/Swiss Franc",
        "Explanation of what this": "Exchange rate between British Pound and Swiss Franc.",
        "Explanation of why it may be important": "Safe-haven cross, impacts UK risk sentiment.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "EURAUD=X",
        "Title": "Euro/Australian Dollar",
        "Explanation of what this": "Exchange rate between Euro and Australian Dollar.",
        "Explanation of why it may be important": "Europe vs. commodity signal, affects trade stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "GBPAUD=X",
        "Title": "Pound/Australian Dollar",
        "Explanation of what this": "Exchange rate between British Pound and Australian Dollar.",
        "Explanation of why it may be important": "UK vs. commodity signal, impacts trade-exposed stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "EURNZD=X",
        "Title": "Euro/New Zealand Dollar",
        "Explanation of what this": "Exchange rate between Euro and New Zealand Dollar.",
        "Explanation of why it may be important": "Europe vs. commodity signal, affects trade trends.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "GBPNZD=X",
        "Title": "Pound/New Zealand Dollar",
        "Explanation of what this": "Exchange rate between British Pound and New Zealand Dollar.",
        "Explanation of why it may be important": "UK vs. commodity signal, impacts trade stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "EURCAD=X",
        "Title": "Euro/Canadian Dollar",
        "Explanation of what this": "Exchange rate between Euro and Canadian Dollar.",
        "Explanation of why it may be important": "Europe vs. commodity signal, affects energy stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "GBPCAD=X",
        "Title": "Pound/Canadian Dollar",
        "Explanation of what this": "Exchange rate between British Pound and Canadian Dollar.",
        "Explanation of why it may be important": "UK vs. commodity signal, impacts energy and trade stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    
    # Currencies (~Forex ~Emerging/Exotic ~USD Base)
    {
        "Symbol": "USDMXN=X",
        "Title": "USD/Mexican Peso",
        "Explanation of what this": "Exchange rate between U.S. Dollar and Mexican Peso.",
        "Explanation of why it may be important": "Emerging market signal, impacts trade and manufacturing stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "USDBRL=X",
        "Title": "USD/Brazilian Real",
        "Explanation of what this": "Exchange rate between U.S. Dollar and Brazilian Real.",
        "Explanation of why it may be important": "Commodity and emerging market signal, affects resource stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "USDZAR=X",
        "Title": "USD/South African Rand",
        "Explanation of what this": "Exchange rate between U.S. Dollar and South African Rand.",
        "Explanation of why it may be important": "Commodity and emerging market signal, impacts mining stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "USDTRY=X",
        "Title": "USD/Turkish Lira",
        "Explanation of what this": "Exchange rate between U.S. Dollar and Turkish Lira.",
        "Explanation of why it may be important": "Emerging market risk signal, affects global sentiment.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "USDINR=X",
        "Title": "USD/Indian Rupee",
        "Explanation of what this": "Exchange rate between U.S. Dollar and Indian Rupee.",
        "Explanation of why it may be important": "Emerging market growth signal, impacts tech and consumer stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "USDKRW=X",
        "Title": "USD/South Korean Won",
        "Explanation of what this": "Exchange rate between U.S. Dollar and South Korean Won.",
        "Explanation of why it may be important": "Tech and export signal, affects semiconductor stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "USDTHB=X",
        "Title": "USD/Thai Baht",
        "Explanation of what this": "Exchange rate between U.S. Dollar and Thai Baht.",
        "Explanation of why it may be important": "Emerging market signal, impacts trade-exposed stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "USDSGD=X",
        "Title": "USD/Singapore Dollar",
        "Explanation of what this": "Exchange rate between U.S. Dollar and Singapore Dollar.",
        "Explanation of why it may be important": "Asian trade hub signal, affects tech and shipping stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "USDHKD=X",
        "Title": "USD/Hong Kong Dollar",
        "Explanation of what this": "Exchange rate between U.S. Dollar and Hong Kong Dollar.",
        "Explanation of why it may be important": "China proxy, impacts Asian market sentiment.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "USDIDR=X",
        "Title": "USD/Indonesian Rupiah",
        "Explanation of what this": "Exchange rate between U.S. Dollar and Indonesian Rupiah.",
        "Explanation of why it may be important": "Emerging market signal, affects commodity stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "USDPHP=X",
        "Title": "USD/Philippine Peso",
        "Explanation of what this": "Exchange rate between U.S. Dollar and Philippine Peso.",
        "Explanation of why it may be important": "Emerging market signal, impacts trade and consumer stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "USDMYR=X",
        "Title": "USD/Malaysian Ringgit",
        "Explanation of what this": "Exchange rate between U.S. Dollar and Malaysian Ringgit.",
        "Explanation of why it may be important": "Emerging market signal, affects commodity and tech stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "USDPLN=X",
        "Title": "USD/Polish Zloty",
        "Explanation of what this": "Exchange rate between U.S. Dollar and Polish Zloty.",
        "Explanation of why it may be important": "Emerging Europe signal, impacts regional equity trends.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "USDRUB=X",
        "Title": "USD/Russian Rubles",
        "Explanation of what this": "Exchange rate between U.S. Dollar and Russian Rubles.",
        "Explanation of why it may be important": "Geopolitical and energy signal, affects commodity stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "USDSEK=X",
        "Title": "USD/Swedish Krona",
        "Explanation of what this": "Exchange rate between U.S. Dollar and Swedish Krona.",
        "Explanation of why it may be important": "European trade signal, impacts industrial stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "USDNOK=X",
        "Title": "USD/Norwegian Krone",
        "Explanation of what this": "Exchange rate between U.S. Dollar and Norwegian Krone.",
        "Explanation of why it may be important": "Oil-linked currency, affects energy stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "USDDKK=X",
        "Title": "USD/Danish Krone",
        "Explanation of what this": "Exchange rate between U.S. Dollar and Danish Krone.",
        "Explanation of why it may be important": "European trade signal, impacts regional stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "USDHUF=X",
        "Title": "USD/Hungarian Forint",
        "Explanation of what this": "Exchange rate between U.S. Dollar and Hungarian Forint.",
        "Explanation of why it may be important": "Emerging Europe signal, affects regional equity trends.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "USDCZK=X",
        "Title": "USD/Czech Koruna",
        "Explanation of what this": "Exchange rate between U.S. Dollar and Czech Koruna.",
        "Explanation of why it may be important": "Emerging Europe signal, impacts manufacturing stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "USDILS=X",
        "Title": "USD/Israeli Shekel",
        "Explanation of what this": "Exchange rate between U.S. Dollar and Israeli Shekel.",
        "Explanation of why it may be important": "Tech and geopolitical signal, affects tech stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "LIBORUSD3M=X",
        "Title": "3-Month LIBOR",
        "Explanation of what this": "3-month London Interbank Offered Rate for USD.",
        "Explanation of why it may be important": "Interbank borrowing cost, predicts credit conditions and stock volatility.",
        "Exchange": "Other (Forex ~check availability)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance (~if not ~FRED ~1-day lag)",
        "Potential Lead": "5-15 days"
    },
    
    # Currencies (~Forex ~More Crosses)
    {
        "Symbol": "CHFJPY=X",
        "Title": "Swiss Franc/Japanese Yen",
        "Explanation of what this": "Exchange rate between Swiss Franc and Japanese Yen.",
        "Explanation of why it may be important": "Safe-haven cross, signals risk-off moves impacting equities.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "CADJPY=X",
        "Title": "Canadian Dollar/Japanese Yen",
        "Explanation of what this": "Exchange rate between Canadian Dollar and Japanese Yen.",
        "Explanation of why it may be important": "Commodity vs. safe-haven signal, affects energy stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "AUDCAD=X",
        "Title": "Australian Dollar/Canadian Dollar",
        "Explanation of what this": "Exchange rate between Australian Dollar and Canadian Dollar.",
        "Explanation of why it may be important": "Commodity cross, impacts resource stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "NZDCAD=X",
        "Title": "New Zealand Dollar/Canadian Dollar",
        "Explanation of what this": "Exchange rate between New Zealand Dollar and Canadian Dollar.",
        "Explanation of why it may be important": "Commodity cross, affects trade-exposed stocks.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "AUDCHF=X",
        "Title": "Australian Dollar/Swiss Franc",
        "Explanation of what this": "Exchange rate between Australian Dollar and Swiss Franc.",
        "Explanation of why it may be important": "Commodity vs. safe-haven signal, impacts risk sentiment.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "NZDCHF=X",
        "Title": "New Zealand Dollar/Swiss Franc",
        "Explanation of what this": "Exchange rate between New Zealand Dollar and Swiss Franc.",
        "Explanation of why it may be important": "Commodity vs. safe-haven signal, affects risk trends.",
        "Exchange": "Other (Forex)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    
    # Equity Indices (~Global)
    {
        "Symbol": "^GSPC",
        "Title": "S&P 500 (US)",
        "Explanation of what this": "Index of 500 large-cap U.S. stocks.",
        "Explanation of why it may be important": "Broad market benchmark, predicts overall equity trends.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "^DJI",
        "Title": "Dow Jones Industrial Average (US)",
        "Explanation of what this": "Index of 30 major U.S. industrial stocks.",
        "Explanation of why it may be important": "Industrial sector signal, leads industrial stock moves.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "^IXIC",
        "Title": "Nasdaq Composite (US)",
        "Explanation of what this": "Index of tech-heavy U.S. stocks.",
        "Explanation of why it may be important": "Tech sector benchmark, predicts tech stock trends.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "^RUT",
        "Title": "Russell 2000 (US small-cap)",
        "Explanation of what this": "Index of U.S. small-cap stocks.",
        "Explanation of why it may be important": "Small-cap signal, leads risk-on/off moves.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "^VIX",
        "Title": "CBOE Volatility Index",
        "Explanation of what this": "Measures expected S&P 500 volatility.",
        "Explanation of why it may be important": "Fear gauge, predicts short-term market reversals.",
        "Exchange": "Other (CBOE)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-3 days"
    },
    {
        "Symbol": "^VXN",
        "Title": "Nasdaq Volatility Index",
        "Explanation of what this": "Measures expected Nasdaq volatility.",
        "Explanation of why it may be important": "Tech volatility signal, leads tech stock moves.",
        "Exchange": "Other (CBOE)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "^FTSE",
        "Title": "FTSE 100 (UK)",
        "Explanation of what this": "Index of 100 major UK stocks.",
        "Explanation of why it may be important": "UK market signal, impacts global equity sentiment.",
        "Exchange": "Other (LSE)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "^N225",
        "Title": "Nikkei 225 (Japan)",
        "Explanation of what this": "Index of 225 major Japanese stocks.",
        "Explanation of why it may be important": "Japan market signal, leads Asian equity trends.",
        "Exchange": "Other (TSE)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "^GDAXI",
        "Title": "DAX (Germany)",
        "Explanation of what this": "Index of 40 major German stocks.",
        "Explanation of why it may be important": "European market signal, impacts industrial stocks.",
        "Exchange": "Other (Xetra)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "^STOXX50E",
        "Title": "Euro STOXX 50 (Europe)",
        "Explanation of what this": "Index of 50 major European stocks.",
        "Explanation of why it may be important": "Broad European signal, predicts regional equity trends.",
        "Exchange": "Other (Euronext)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "000001.SS",
        "Title": "Shanghai Composite (China)",
        "Explanation of what this": "Index of major Chinese stocks.",
        "Explanation of why it may be important": "China market signal, impacts emerging market stocks.",
        "Exchange": "Other (SSE)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-20 days"
    },
    {
        "Symbol": "^BVSP",
        "Title": "Bovespa (Brazil)",
        "Explanation of what this": "Index of major Brazilian stocks.",
        "Explanation of why it may be important": "Emerging market signal, affects commodity stocks.",
        "Exchange": "Other (B3)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "^HSI",
        "Title": "Hang Seng Index (Hong Kong)",
        "Explanation of what this": "Index of major Hong Kong stocks.",
        "Explanation of why it may be important": "Asian market signal, impacts China-exposed stocks.",
        "Exchange": "Other (HKEX)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-20 days"
    },
    {
        "Symbol": "^BSESN",
        "Title": "BSE Sensex (India)",
        "Explanation of what this": "Index of 30 major Indian stocks.",
        "Explanation of why it may be important": "India growth signal, leads tech and consumer stocks.",
        "Exchange": "Other (BSE)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "^NYAD",
        "Title": "NYSE Advance-Decline Line",
        "Explanation of what this": "Net number of advancing vs. declining NYSE stocks.",
        "Explanation of why it may be important": "Market breadth signal, predicts short-term trends.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    
    # Treasury Yields (~Bond Yields/Interest Rates)
    {
        "Symbol": "^IRX",
        "Title": "13-week Treasury Bill Yield",
        "Explanation of what this": "Yield on 13-week U.S. Treasury bills.",
        "Explanation of why it may be important": "Short-term rate signal, impacts yield curve and stock risk premium.",
        "Exchange": "Other (Treasury)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "^UST2Y",
        "Title": "2-Year Treasury Yield",
        "Explanation of what this": "Yield on 2-year U.S. Treasury notes.",
        "Explanation of why it may be important": "Short-term rate signal, affects financial and rate-sensitive stocks.",
        "Exchange": "Other (Treasury)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "^FVX",
        "Title": "5-Year Treasury Yield",
        "Explanation of what this": "Yield on 5-year U.S. Treasury notes.",
        "Explanation of why it may be important": "Mid-term rate signal, predicts economic growth expectations.",
        "Exchange": "Other (Treasury)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "^TNX",
        "Title": "10-Year Treasury Yield",
        "Explanation of what this": "Yield on 10-year U.S. Treasury notes.",
        "Explanation of why it may be important": "Benchmark rate, impacts equity valuations and yield spreads.",
        "Exchange": "Other (Treasury)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-30 days"
    },
    {
        "Symbol": "^TYX",
        "Title": "30-Year Treasury Yield",
        "Explanation of what this": "Yield on 30-year U.S. Treasury bonds.",
        "Explanation of why it may be important": "Long-term rate signal, affects long-term investment trends.",
        "Exchange": "Other (Treasury)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "15-30+ days"
    },
    
    # Cryptocurrencies
    {
        "Symbol": "BTC-USD",
        "Title": "Bitcoin",
        "Explanation of what this": "Price of Bitcoin in USD.",
        "Explanation of why it may be important": "Risk appetite signal, impacts crypto-related and tech stocks.",
        "Exchange": "Other (Crypto)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "ETH-USD",
        "Title": "Ethereum",
        "Explanation of what this": "Price of Ethereum in USD.",
        "Explanation of why it may be important": "Altcoin risk signal, predicts speculative stock moves.",
        "Exchange": "Other (Crypto)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "LTC-USD",
        "Title": "Litecoin",
        "Explanation of what this": "Price of Litecoin in USD.",
        "Explanation of why it may be important": "Crypto sentiment signal, impacts risk appetite trends.",
        "Exchange": "Other (Crypto)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "XRP-USD",
        "Title": "Ripple XRP",
        "Explanation of what this": "Price of Ripple XRP in USD.",
        "Explanation of why it may be important": "Crypto adoption signal, predicts fintech stock moves.",
        "Exchange": "Other (Crypto)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "ADA-USD",
        "Title": "Cardano ADA",
        "Explanation of what this": "Price of Cardano ADA in USD.",
        "Explanation of why it may be important": "Altcoin signal, impacts speculative equity trends.",
        "Exchange": "Other (Crypto)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "SOL-USD",
        "Title": "Solana SOL",
        "Explanation of what this": "Price of Solana SOL in USD.",
        "Explanation of why it may be important": "Crypto innovation signal, predicts tech stock sentiment.",
        "Exchange": "Other (Crypto)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    
    # Sector ETFs (~U.S. Equity Sectors)
    {
        "Symbol": "XLK",
        "Title": "Technology Sector ETF",
        "Explanation of what this": "ETF tracking U.S. technology stocks.",
        "Explanation of why it may be important": "Tech sector benchmark, leads tech stock performance.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "XLV",
        "Title": "Health Care Sector ETF",
        "Explanation of what this": "ETF tracking U.S. health care stocks.",
        "Explanation of why it may be important": "Health care signal, predicts biotech and pharma trends.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "XLE",
        "Title": "Energy Sector ETF",
        "Explanation of what this": "ETF tracking U.S. energy stocks.",
        "Explanation of why it may be important": "Energy sector signal, leads oil and gas stock moves.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "XLF",
        "Title": "Financial Sector ETF",
        "Explanation of what this": "ETF tracking U.S. financial stocks.",
        "Explanation of why it may be important": "Financial sector signal, predicts bank and insurance trends.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "XLI",
        "Title": "Industrial Sector ETF",
        "Explanation of what this": "ETF tracking U.S. industrial stocks.",
        "Explanation of why it may be important": "Industrial signal, leads manufacturing stock performance.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "XLP",
        "Title": "Consumer Staples Sector ETF",
        "Explanation of what this": "ETF tracking U.S. consumer staples stocks.",
        "Explanation of why it may be important": "Defensive signal, predicts consumer stability trends.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "XLB",
        "Title": "Materials Sector ETF",
        "Explanation of what this": "ETF tracking U.S. materials stocks.",
        "Explanation of why it may be important": "Materials signal, leads mining and industrial stocks.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "XLRE",
        "Title": "Real Estate Sector ETF",
        "Explanation of what this": "ETF tracking U.S. real estate stocks.",
        "Explanation of why it may be important": "Real estate signal, predicts housing and REIT trends.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "XLU",
        "Title": "Utilities Sector ETF",
        "Explanation of what this": "ETF tracking U.S. utilities stocks.",
        "Explanation of why it may be important": "Defensive signal, impacts utility stock performance.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "XLY",
        "Title": "Consumer Discretionary Sector ETF",
        "Explanation of what this": "ETF tracking U.S. consumer discretionary stocks.",
        "Explanation of why it may be important": "Consumer spending signal, leads retail and luxury stocks.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "SMH",
        "Title": "Semiconductor ETF",
        "Explanation of what this": "ETF tracking U.S. semiconductor stocks.",
        "Explanation of why it may be important": "Chip demand signal, predicts tech stock trends.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "IYT",
        "Title": "Transportation ETF",
        "Explanation of what this": "ETF tracking U.S. transportation stocks.",
        "Explanation of why it may be important": "Economic activity signal, leads transport and logistics stocks.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    
    # Economic Indicators (~Leading & Sentiment)
    {
        "Symbol": "^MOVE",
        "Title": "MOVE Index",
        "Explanation of what this": "Index measuring Treasury yield volatility.",
        "Explanation of why it may be important": "Bond market stress signal, predicts equity volatility.",
        "Exchange": "Other (ICE)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "^OVX",
        "Title": "Crude Oil Volatility Index",
        "Explanation of what this": "Measures expected oil price volatility.",
        "Explanation of why it may be important": "Energy market uncertainty, leads energy stock moves.",
        "Exchange": "Other (CBOE)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "^GVZ",
        "Title": "Gold Volatility Index",
        "Explanation of what this": "Measures expected gold price volatility.",
        "Explanation of why it may be important": "Safe-haven volatility, predicts risk-off equity shifts.",
        "Exchange": "Other (CBOE)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "EMHY",
        "Title": "Emerging Market High Yield Bond ETF",
        "Explanation of what this": "ETF tracking high-yield emerging market bonds.",
        "Explanation of why it may be important": "Risk appetite signal, leads emerging market stock trends.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "BKLN",
        "Title": "Senior Loan ETF",
        "Explanation of what this": "ETF tracking senior loans.",
        "Explanation of why it may be important": "Credit conditions signal, predicts financial stock moves.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "ITB",
        "Title": "U.S. Home Construction ETF",
        "Explanation of what this": "ETF tracking U.S. home construction stocks.",
        "Explanation of why it may be important": "Housing market signal, leads real estate and consumer stocks.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-30 days"
    },
    {
        "Symbol": "PAYX",
        "Title": "Paychex Stock",
        "Explanation of what this": "Stock price of Paychex, a payroll processing company.",
        "Explanation of why it may be important": "Payroll proxy, predicts small business employment trends.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "ADP",
        "Title": "ADP Stock",
        "Explanation of what this": "Stock price of Automatic Data Processing, a payroll company.",
        "Explanation of why it may be important": "Employment signal, predicts broader economic trends.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "AMZN",
        "Title": "Amazon Stock",
        "Explanation of what this": "Stock price of Amazon, an e-commerce giant.",
        "Explanation of why it may be important": "E-commerce signal, leads consumer discretionary trends.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "FDX",
        "Title": "FedEx Stock",
        "Explanation of what this": "Stock price of FedEx, a logistics company.",
        "Explanation of why it may be important": "Shipping signal, predicts economic activity and transport stocks.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "ASHR",
        "Title": "China A-shares ETF",
        "Explanation of what this": "ETF tracking mainland China A-shares.",
        "Explanation of why it may be important": "China equity signal, leads emerging market trends.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-20 days"
    },
    {
        "Symbol": "MCHI",
        "Title": "MSCI China ETF",
        "Explanation of what this": "ETF tracking broad Chinese equities.",
        "Explanation of why it may be important": "China market signal, predicts China-exposed stock moves.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-20 days"
    },
    
    A# Credit Market & Yield Curve Indicators
    {
        "Symbol": "SHY",
        "Title": "1-3 Year Treasury Bond ETF",
        "Explanation of what this": "ETF tracking 1-3 year U.S. Treasury bonds.",
        "Explanation of why it may be important": "Short-term rate signal, impacts yield curve and stock risk.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "SHYG",
        "Title": "0-5 Year High Yield Corporate Bond ETF",
        "Explanation of what this": "ETF tracking short-term high-yield corporate bonds.",
        "Explanation of why it may be important": "Short-term credit signal, predicts risk appetite shifts.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "MUB",
        "Title": "Municipal Bond ETF",
        "Explanation of what this": "ETF tracking U.S. municipal bonds.",
        "Explanation of why it may be important": "Municipal health signal, impacts credit-sensitive stocks.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    
    # Global & Geopolitical Indicators
    {
        "Symbol": "ACWX",
        "Title": "Global ex-U.S. Equity ETF",
        "Explanation of what this": "ETF tracking global equities excluding U.S.",
        "Explanation of why it may be important": "Global market signal, predicts U.S. equity trends.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "FXI",
        "Title": "China Large-Cap ETF",
        "Explanation of what this": "ETF tracking large-cap Chinese stocks.",
        "Explanation of why it may be important": "China market signal, impacts global equity sentiment.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "EWJ",
        "Title": "Japan ETF",
        "Explanation of what this": "ETF tracking Japanese equities.",
        "Explanation of why it may be important": "Japan market signal, leads Asian equity trends.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "EWG",
        "Title": "Germany ETF",
        "Explanation of what this": "ETF tracking German equities.",
        "Explanation of why it may be important": "European market signal, impacts industrial stocks.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "EWZ",
        "Title": "Brazil ETF",
        "Explanation of what this": "ETF tracking Brazilian equities.",
        "Explanation of why it may be important": "Emerging market signal, leads commodity stock trends.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "INDA",
        "Title": "India ETF",
        "Explanation of what this": "ETF tracking Indian equities.",
        "Explanation of why it may be important": "India growth signal, predicts tech and consumer stock moves.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    
    # Other Macro & Economic ETFs
    {
        "Symbol": "DX-Y.NYB",
        "Title": "U.S. Dollar Index",
        "Explanation of what this": "Index measuring USD against a basket of currencies.",
        "Explanation of why it may be important": "Dollar strength signal, impacts global trade and equity valuations.",
        "Exchange": "Other (ICE)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "TIP",
        "Title": "TIPS Bond ETF",
        "Explanation of what this": "ETF tracking Treasury Inflation-Protected Securities.",
        "Explanation of why it may be important": "Inflation signal, predicts equity risk premium shifts.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "EEM",
        "Title": "Emerging Markets ETF",
        "Explanation of what this": "ETF tracking emerging market equities.",
        "Explanation of why it may be important": "Emerging market signal, leads global risk appetite trends.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "HYG",
        "Title": "High Yield Bond ETF",
        "Explanation of what this": "ETF tracking high-yield corporate bonds.",
        "Explanation of why it may be important": "Credit risk signal, predicts equity risk appetite.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "LQD",
        "Title": "Investment Grade Corporate Bond ETF",
        "Explanation of what this": "ETF tracking investment-grade corporate bonds.",
        "Explanation of why it may be important": "Credit stability signal, impacts equity valuations.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "IEF",
        "Title": "7-10 Year Treasury Bond ETF",
        "Explanation of what this": "ETF tracking 7-10 year U.S. Treasury bonds.",
        "Explanation of why it may be important": "Mid-term rate signal, predicts equity risk shifts.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "TLT",
        "Title": "20+ Year Treasury Bond ETF",
        "Explanation of what this": "ETF tracking 20+ year U.S. Treasury bonds.",
        "Explanation of why it may be important": "Long-term rate signal, impacts equity valuations.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "15-30+ days"
    },
    {
        "Symbol": "ICLN",
        "Title": "Clean Energy ETF",
        "Explanation of what this": "ETF tracking clean energy companies.",
        "Explanation of why it may be important": "Sustainable investing signal, predicts policy-driven trends.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "JNK",
        "Title": "High Yield Bond ETF",
        "Explanation of what this": "ETF tracking high-yield corporate bonds.",
        "Explanation of why it may be important": "Credit risk signal, predicts short-term equity shifts.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "EMB",
        "Title": "Emerging Market Bond ETF",
        "Explanation of what this": "ETF tracking emerging market bonds.",
        "Explanation of why it may be important": "Global risk signal, leads emerging market equity trends.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "XHB",
        "Title": "Homebuilders ETF",
        "Explanation of what this": "ETF tracking U.S. homebuilder stocks.",
        "Explanation of why it may be important": "Housing market signal, predicts consumer and real estate trends.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "SOXX",
        "Title": "Semiconductor ETF",
        "Explanation of what this": "ETF tracking semiconductor stocks.",
        "Explanation of why it may be important": "Chip demand signal, leads tech stock performance.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "COPX",
        "Title": "Global Copper Miners ETF",
        "Explanation of what this": "ETF tracking global copper mining companies.",
        "Explanation of why it may be important": "Economic growth and inflation signal, leads industrial and mining stocks (e.g., FCX).",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "ITA",
        "Title": "Defense Stocks ETF",
        "Explanation of what this": "ETF tracking U.S. aerospace and defense stocks.",
        "Explanation of why it may be important": "Geopolitical tension signal, predicts defense stock moves (e.g., LMT) during uncertainty.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "CEW",
        "Title": "Emerging Market FX ETF",
        "Explanation of what this": "ETF tracking emerging market currency performance.",
        "Explanation of why it may be important": "Global risk appetite signal, leads emerging market stock trends.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "KBE",
        "Title": "S&P Bank ETF",
        "Explanation of what this": "ETF tracking U.S. bank stocks.",
        "Explanation of why it may be important": "Rate-sensitive signal, predicts bank stock performance (e.g., BAC) with interest rate shifts.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "TAN",
        "Title": "Solar ETF",
        "Explanation of what this": "ETF tracking solar energy companies.",
        "Explanation of why it may be important": "Sustainable investing signal, leads solar and green tech stocks (e.g., ENPH) with policy shifts.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "PBW",
        "Title": "Clean Energy ETF",
        "Explanation of what this": "ETF tracking clean energy companies.",
        "Explanation of why it may be important": "Policy-driven signal, predicts clean energy stock trends with regulatory changes.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "SKYY",
        "Title": "Cloud Computing ETF",
        "Explanation of what this": "ETF tracking cloud computing companies.",
        "Explanation of why it may be important": "Tech innovation signal, leads cloud tech stocks (e.g., CRM) with demand shifts.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "HACK",
        "Title": "Cybersecurity ETF",
        "Explanation of what this": "ETF tracking cybersecurity companies.",
        "Explanation of why it may be important": "Tech security signal, predicts cybersecurity stock moves (e.g., CRWD) with threat levels.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "FINX",
        "Title": "Fintech ETF",
        "Explanation of what this": "ETF tracking fintech companies.",
        "Explanation of why it may be important": "Financial innovation signal, leads fintech stock trends (e.g., SQ) with adoption shifts.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    
    # Volatility & Sentiment Indicators
    {
        "Symbol": "^VVIX",
        "Title": "Volatility of VIX Index",
        "Explanation of what this": "Index measuring volatility of the VIX.",
        "Explanation of why it may be important": "Volatility stress signal, predicts short-term equity volatility spikes.",
        "Exchange": "Other (CBOE)",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "VXX",
        "Title": "Short-term VIX ETF",
        "Explanation of what this": "ETF tracking short-term VIX futures.",
        "Explanation of why it may be important": "Fear gauge proxy, predicts near-term equity reversals.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-3 days"
    },
    # Commented out due to uncertainty in Yahoo availability
     {
         "Symbol": "^SKEW",
         "Title": "SKEW Index",
         "Explanation of what this": "Index measuring tail risk of S&P 500.",
         "Explanation of why it may be important": "Extreme move signal, predicts potential sharp equity drops.",
         "Exchange": "Other (CBOE)",
         "Type": "Daily",
         "Lag number": 0,
         "Source": "YFinance (~iffy ~check)",
         "Potential Lead": "1-3 days"
    },
    
    # Interest Rate & Monetary Policy Proxies
    {
        "Symbol": "BIL",
        "Title": "1-3 Month Treasury Bill ETF",
        "Explanation of what this": "ETF tracking 1-3 month U.S. Treasury bills.",
        "Explanation of why it may be important": "Shortest-term rate signal, predicts immediate rate shifts impacting stocks.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "STIP",
        "Title": "0-5 Year TIPS Bond ETF",
        "Explanation of what this": "ETF tracking 0-5 year Treasury Inflation-Protected Securities.",
        "Explanation of why it may be important": "Short-term inflation signal, predicts equity risk adjustments.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "SHV",
        "Title": "Short-term Treasury ETF",
        "Explanation of what this": "ETF tracking short-term U.S. Treasury securities.",
        "Explanation of why it may be important": "Short-term rate proxy, impacts financial stock sensitivity.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    
    # Inflation & Economic Activity Indicators
    {
        "Symbol": "RINF",
        "Title": "Inflation Expectations ETF",
        "Explanation of what this": "ETF tracking inflation expectations.",
        "Explanation of why it may be important": "Inflation signal, predicts equity reactions to rate expectations.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "BDRY",
        "Title": "Dry Bulk Shipping ETF",
        "Explanation of what this": "ETF tracking dry bulk shipping companies.",
        "Explanation of why it may be important": "Economic activity proxy, leads transport and industrial stock trends.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "JJC",
        "Title": "Copper ETF",
        "Explanation of what this": "ETF tracking copper prices.",
        "Explanation of why it may be important": "Economic growth signal, predicts industrial stock performance.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "XME",
        "Title": "Metals & Mining ETF",
        "Explanation of what this": "ETF tracking metals and mining companies.",
        "Explanation of why it may be important": "Resource demand signal, leads mining stock trends.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    
    # Transportation & Supply Chain Indicators
    {
        "Symbol": "^DJT",
        "Title": "Dow Jones Transportation Average",
        "Explanation of what this": "Index of 20 major U.S. transportation stocks.",
        "Explanation of why it may be important": "Economic activity signal, leads transport and logistics stock trends.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    
    # Market Internals and Breadth Indicators
    {
        "Symbol": "^NYHILO",
        "Title": "NYSE New Highs-New Lows",
        "Explanation of what this": "Index of NYSE stocks hitting new highs vs. lows.",
        "Explanation of why it may be important": "Market momentum signal, predicts short-term equity trends.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "^TICK",
        "Title": "NYSE Tick Index",
        "Explanation of what this": "Index measuring net upticks vs. downticks on NYSE.",
        "Explanation of why it may be important": "Short-term momentum signal, predicts immediate equity reversals.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-3 days"
    },
    {
        "Symbol": "^TRIN",
        "Title": "Arms Index",
        "Explanation of what this": "Index measuring buying vs. selling intensity on NYSE.",
        "Explanation of why it may be important": "Overbought/oversold signal, predicts short-term equity shifts.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-3 days"
    },
    
    # Real Estate & Infrastructure
    {
        "Symbol": "VNQ",
        "Title": "Real Estate ETF",
        "Explanation of what this": "ETF tracking U.S. real estate investment trusts (REITs).",
        "Explanation of why it may be important": "Real estate signal, predicts REIT and housing stock trends.",
        "Exchange": "NYSE",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "PAVE",
        "Title": "Infrastructure ETF",
        "Explanation of what this": "ETF tracking U.S. infrastructure companies.",
        "Explanation of why it may be important": "Infrastructure spending signal, leads industrial stock trends.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    
    # ESG & Thematic ETFs
    {
        "Symbol": "ESGU",
        "Title": "ESG-aware ETF",
        "Explanation of what this": "ETF tracking ESG-focused U.S. companies.",
        "Explanation of why it may be important": "Sustainable investing signal, predicts ESG stock trends.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "ARKK",
        "Title": "ARK Innovation ETF",
        "Explanation of what this": "ETF tracking high-growth innovative companies.",
        "Explanation of why it may be important": "Innovation signal, leads speculative tech stock trends.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "AIQ",
        "Title": "Artificial Intelligence ETF",
        "Explanation of what this": "ETF tracking AI-focused companies.",
        "Explanation of why it may be important": "AI innovation signal, predicts tech stock performance.",
        "Exchange": "NASDAQ",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    
    # Calculations (~Yield Curve Spreads ~Risk & Growth ~5-30+ Days)
    {
        "Symbol": "^TNX - ^IRX",
        "Title": "10-Year minus 3-Month Treasury Yield Spread",
        "Explanation of what this": "Calculated spread between 10-year and 3-month Treasury yields.",
        "Explanation of why it may be important": "Yield curve signal, predicts recessions (inversion) or growth, impacting all stocks.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-30 days"
    },
    {
        "Symbol": "^FVX - ^IRX",
        "Title": "5-Year minus 3-Month Treasury Yield Spread",
        "Explanation of what this": "Calculated spread between 5-year and 3-month Treasury yields.",
        "Explanation of why it may be important": "Mid-term yield signal, predicts growth expectations affecting stocks.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "^TYX - ^UST2Y",
        "Title": "30-Year minus 2-Year Treasury Yield Spread",
        "Explanation of what this": "Calculated spread between 30-year and 2-year Treasury yields.",
        "Explanation of why it may be important": "Long-term yield signal, predicts economic outlook impacting stocks.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "15-30+ days"
    },
    {
        "Symbol": "^TNX - ^UST2Y",
        "Title": "10-Year minus 2-Year Treasury Yield Spread",
        "Explanation of what this": "Calculated spread between 10-year and 2-year Treasury yields.",
        "Explanation of why it may be important": "Classic yield curve signal, predicts recessions and stock adjustments.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-30 days"
    },
    {
        "Symbol": "TIP / TLT",
        "Title": "TIPS vs. Long-Term Treasury Ratio",
        "Explanation of what this": "Calculated ratio of TIPS ETF to long-term Treasury ETF.",
        "Explanation of why it may be important": "Inflation expectation signal, predicts equity risk premium shifts.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "TIP - ^TNX",
        "Title": "10-Year Real Yield",
        "Explanation of what this": "Calculated difference between TIPS ETF and 10-year Treasury yield.",
        "Explanation of why it may be important": "Real yield signal, predicts equity risk premium shifts (proxy for DGS10YBE).",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-20 days"
    },
    
    # Calculations (~Commodity Ratios ~Economic Activity ~5-15+ Days)
    {
        "Symbol": "HG=F / GLD",
        "Title": "Copper-to-Gold Ratio",
        "Explanation of what this": "Calculated ratio of copper futures to gold ETF.",
        "Explanation of why it may be important": "Growth signal, high ratio predicts industrial stock strength.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "LB=F / GLD",
        "Title": "Lumber-to-Gold Ratio",
        "Explanation of what this": "Calculated ratio of lumber futures to gold ETF.",
        "Explanation of why it may be important": "Housing signal, high ratio predicts real estate stock trends.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "CL=F / GC=F",
        "Title": "Oil-to-Gold Ratio",
        "Explanation of what this": "Calculated ratio of WTI oil futures to gold futures.",
        "Explanation of why it may be important": "Energy signal, high ratio predicts energy stock strength.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-10 days"
    },
    {
        "Symbol": "SI=F / GC=F",
        "Title": "Silver-to-Gold Ratio",
        "Explanation of what this": "Calculated ratio of silver futures to gold futures.",
        "Explanation of why it may be important": "Risk signal, high ratio predicts industrial stock trends.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-10 days"
    },
    {
        "Symbol": "ETH-USD / BTC-USD",
        "Title": "Ethereum-to-Bitcoin Ratio",
        "Explanation of what this": "Calculated ratio of Ethereum to Bitcoin prices.",
        "Explanation of why it may be important": "Crypto risk signal, high ratio predicts altcoin and speculative stock moves.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    
    # Calculations (~Credit Market Spreads ~Risk Appetite ~1-5+ Days)
    {
        "Symbol": "HYG - LQD",
        "Title": "High Yield minus Investment Grade Bond Spread",
        "Explanation of what this": "Calculated spread between high-yield and investment-grade bond ETFs.",
        "Explanation of why it may be important": "Credit risk signal, widening predicts equity downturns.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "JNK - LQD",
        "Title": "High Yield minus Investment Grade Bond Spread (Alternate)",
        "Explanation of what this": "Calculated spread between alternate high-yield and investment-grade bond ETFs.",
        "Explanation of why it may be important": "Credit risk signal, predicts equity risk appetite shifts.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "SHYG - SHY",
        "Title": "Short-Term High Yield minus Treasury Spread",
        "Explanation of what this": "Calculated spread between short-term high-yield and Treasury ETFs.",
        "Explanation of why it may be important": "Short-term credit signal, predicts near-term equity risk shifts.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-3 days"
    },
    
    # Calculations (~Sector vs. Market Ratios ~Relative Strength ~1-5 Days)
    {
        "Symbol": "XLK / ^GSPC",
        "Title": "Tech vs. S&P 500 Ratio",
        "Explanation of what this": "Calculated ratio of tech ETF to S&P 500 index.",
        "Explanation of why it may be important": "Tech strength signal, predicts tech stock outperformance.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "XLE / ^GSPC",
        "Title": "Energy vs. S&P 500 Ratio",
        "Explanation of what this": "Calculated ratio of energy ETF to S&P 500 index.",
        "Explanation of why it may be important": "Energy strength signal, predicts energy stock trends.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "XLF / ^GSPC",
        "Title": "Financials vs. S&P 500 Ratio",
        "Explanation of what this": "Calculated ratio of financial ETF to S&P 500 index.",
        "Explanation of why it may be important": "Financial strength signal, predicts bank stock performance.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "XLY / XLP",
        "Title": "Consumer Discretionary vs. Staples Ratio",
        "Explanation of what this": "Calculated ratio of discretionary to staples ETFs.",
        "Explanation of why it may be important": "Risk appetite signal, high ratio predicts discretionary stock strength.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "XME / XLB",
        "Title": "Metals & Mining vs. Materials Ratio",
        "Explanation of what this": "Calculated ratio of mining to materials ETFs.",
        "Explanation of why it may be important": "Mining strength signal, predicts mining stock outperformance.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "XLV / XBI",
        "Title": "Health Care vs. Biotech Ratio",
        "Explanation of what this": "Calculated ratio of health care to biotech ETFs.",
        "Explanation of why it may be important": "Biotech strength signal, predicts biotech stock trends.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    
    # Calculations (~Volatility Spreads ~Sentiment ~1-3+ Days)
    {
        "Symbol": "^VIX - VXX",
        "Title": "Spot VIX minus Futures Spread",
        "Explanation of what this": "Calculated spread between spot VIX and short-term VIX futures ETF.",
        "Explanation of why it may be important": "Contango signal, predicts short-term equity volatility shifts.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-3 days"
    },
    {
        "Symbol": "^VXN - ^VIX",
        "Title": "Nasdaq VIX minus CBOE VIX Spread",
        "Explanation of what this": "Calculated spread between Nasdaq and CBOE volatility indices.",
        "Explanation of why it may be important": "Tech volatility signal, predicts tech stock movements.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-3 days"
    },
    {
        "Symbol": "^OVX - ^VIX",
        "Title": "Oil Volatility minus CBOE VIX Spread",
        "Explanation of what this": "Calculated spread between oil and CBOE volatility indices.",
        "Explanation of why it may be important": "Energy volatility signal, predicts energy stock trends.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-3 days"
    },
    {
        "Symbol": "^VIX / ^VVIX",
        "Title": "VIX-to-VVIX Ratio",
        "Explanation of what this": "Calculated ratio of VIX to its volatility index.",
        "Explanation of why it may be important": "Volatility calm/stress signal, predicts equity stability shifts.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-3 days"
    },
    
    # Calculations (~Global Risk Ratios ~Geopolitical ~3-10+ Days)
    {
        "Symbol": "GLD / BTC-USD",
        "Title": "Gold-to-Bitcoin Ratio",
        "Explanation of what this": "Calculated ratio of gold ETF to Bitcoin price.",
        "Explanation of why it may be important": "Safe-haven signal, high ratio predicts risk-off equity moves.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    {
        "Symbol": "EEM / ^GSPC",
        "Title": "Emerging Markets vs. S&P 500 Ratio",
        "Explanation of what this": "Calculated ratio of emerging markets ETF to S&P 500 index.",
        "Explanation of why it may be important": "Global risk signal, predicts risk-on/off equity trends.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "3-10 days"
    },
    
    # Calculations (~Stock-Specific Proxies ~Peer Influence ~1-5 Days)
    {
        "Symbol": "SOXX / SMH",
        "Title": "Semiconductor ETF Ratio",
        "Explanation of what this": "Calculated ratio of two semiconductor ETFs.",
        "Explanation of why it may be important": "Chip sector signal, predicts relative semiconductor stock trends.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "XOP / XLE",
        "Title": "Oil Exploration vs. Energy Ratio",
        "Explanation of what this": "Calculated ratio of oil exploration to energy sector ETFs.",
        "Explanation of why it may be important": "Energy subsector signal, predicts oil stock performance.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    
    # Calculations (~Momentum & Breadth ~Market Internals ~1-5 Days)
    {
        "Symbol": "^NYAD - ^NYAD[-1]",
        "Title": "Advance-Decline Daily Change",
        "Explanation of what this": "Calculated daily change in NYSE Advance-Decline Line.",
        "Explanation of why it may be important": "Momentum signal, predicts short-term equity trend shifts.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-3 days"
    },
    {
        "Symbol": "^TICK - ^TICK[-1]",
        "Title": "NYSE Tick Daily Change",
        "Explanation of what this": "Calculated daily change in NYSE Tick Index.",
        "Explanation of why it may be important": "Short-term momentum signal, predicts immediate equity reversals.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-3 days"
    },
    {
        "Symbol": "^TRIN - 1",
        "Title": "Arms Index Deviation",
        "Explanation of what this": "Calculated deviation of Arms Index from neutral (1).",
        "Explanation of why it may be important": "Overbought/oversold signal, predicts short-term equity shifts.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-3 days"
    },
    {
        "Symbol": "^DJI - ^DJI[-5]",
        "Title": "Dow Jones 5-Day Change",
        "Explanation of what this": "Calculated 5-day change in Dow Jones Industrial Average.",
        "Explanation of why it may be important": "Industrial momentum signal, predicts industrial stock trends.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "^IXIC - ^IXIC[-5]",
        "Title": "Nasdaq 5-Day Change",
        "Explanation of what this": "Calculated 5-day change in Nasdaq Composite.",
        "Explanation of why it may be important": "Tech momentum signal, predicts tech stock trends.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    {
        "Symbol": "BDRY - BDRY[-5]",
        "Title": "Baltic Dry 5-Day Change",
        "Explanation of what this": "Calculated 5-day change in Baltic Dry Shipping ETF.",
        "Explanation of why it may be important": "Shipping momentum signal, predicts transport stock trends.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-10 days"
    },
    
    # Calculations (~Employment & Consumer Signals ~5-15+ Days)
    {
        "Symbol": "PAYX - ADP",
        "Title": "Paychex minus ADP Spread",
        "Explanation of what this": "Calculated spread between Paychex and ADP stock prices.",
        "Explanation of why it may be important": "Employment signal, predicts small vs. large firm employment trends.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "AMZN / XRT",
        "Title": "Amazon vs. Retail Ratio",
        "Explanation of what this": "Calculated ratio of Amazon stock to Retail ETF.",
        "Explanation of why it may be important": "E-commerce signal, predicts online vs. traditional retail trends.",
        "Exchange": "Calculated",
        "Type": "Daily",
        "Lag number": 0,
        "Source": "YFinance",
        "Potential Lead": "1-5 days"
    },
    
    # Non-Yahoo Indicators (~Macroeconomic Surprises & Expectations ~5-15 Days)
    {
        "Symbol": "CESIUSD",
        "Title": "Citi Economic Surprise Index",
        "Explanation of what this": "Index measuring U.S. economic data deviations from consensus expectations.",
        "Explanation of why it may be important": "Surprise signal, high values predict short-term equity upturns.",
        "Exchange": "Other (Citi)",
        "Type": "Daily",
        "Lag number": 1,
        "Source": "Other (Citi ~external fetch)",
        "Potential Lead": "5-15 days"
    },
    
    # Non-Yahoo Indicators (~Inflation Expectations and Rates ~5-15 Days)
    {
        "Symbol": "T5YIE",
        "Title": "5-Year Breakeven Inflation Rate",
        "Explanation of what this": "Market-based measure of 5-year inflation expectations.",
        "Explanation of why it may be important": "Inflation signal, rising rates predict Fed actions impacting stocks (proxy for DGS5YBE).",
        "Exchange": "Other (FRED)",
        "Type": "Daily",
        "Lag number": 1,
        "Source": "FRED",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "T10YIE",
        "Title": "10-Year Breakeven Inflation Rate",
        "Explanation of what this": "Market-based measure of 10-year inflation expectations.",
        "Explanation of why it may be important": "Inflation signal, rising rates predict equity adjustments (proxy for DGS10YBE).",
        "Exchange": "Other (FRED)",
        "Type": "Daily",
        "Lag number": 1,
        "Source": "FRED",
        "Potential Lead": "5-15 days"
    },
    
    # Non-Yahoo Indicators (~Employment & Wage Indicators ~10-20 Days)
    {
        "Symbol": "ICSA",
        "Title": "Initial Jobless Claims",
        "Explanation of what this": "Weekly count of initial U.S. jobless claims.",
        "Explanation of why it may be important": "Employment signal, low claims predict consumer spending and stock upturns.",
        "Exchange": "Other (FRED)",
        "Type": "Weekly",
        "Lag number": 7,
        "Source": "FRED",
        "Potential Lead": "10-20 days"
    },
    {
        "Symbol": "CCSA",
        "Title": "Continued Jobless Claims",
        "Explanation of what this": "Weekly count of continued U.S. jobless claims.",
        "Explanation of why it may be important": "Employment stability signal, low claims predict stock strength.",
        "Exchange": "Other (FRED)",
        "Type": "Weekly",
        "Lag number": 7,
        "Source": "FRED",
        "Potential Lead": "10-20 days"
    },
    
    # Non-Yahoo Indicators (~Consumer Sentiment & Confidence ~5-30 Days)
    {
        "Symbol": "UMCSENT",
        "Title": "U. Michigan Consumer Sentiment Index",
        "Explanation of what this": "Monthly survey of U.S. consumer sentiment.",
        "Explanation of why it may be important": "Consumer confidence signal, predicts discretionary spending and stock trends.",
        "Exchange": "Other (FRED)",
        "Type": "Monthly",
        "Lag number": 14-28,
        "Source": "FRED",
        "Potential Lead": "5-30 days"
    },
    {
        "Symbol": "CSCICP03USM665S",
        "Title": "OECD Composite Leading Indicator U.S.",
        "Explanation of what this": "Monthly composite leading indicator for the U.S. economy.",
        "Explanation of why it may be important": "Economic leading signal, predicts broad stock market trends.",
        "Exchange": "Other (FRED)",
        "Type": "Monthly",
        "Lag number": 30,
        "Source": "FRED",
        "Potential Lead": "5-30 days"
    },
    
    # Non-Yahoo Indicators (~Housing Market Strength ~5-20 Days)
    {
        "Symbol": "HMI",
        "Title": "NAHB Housing Market Index",
        "Explanation of what this": "Monthly index of U.S. builder sentiment.",
        "Explanation of why it may be important": "Housing market signal, predicts real estate stock trends (e.g., DHI).",
        "Exchange": "Other (NAHB)",
        "Type": "Monthly",
        "Lag number": 7-14,
        "Source": "Other (NAHB ~external fetch)",
        "Potential Lead": "5-20 days"
    },
    
    # Non-Yahoo Indicators (~Retail Sales & Consumption ~5-15 Days)
    {
        "Symbol": "RSAFS",
        "Title": "U.S. Retail Sales",
        "Explanation of what this": "Monthly advance U.S. retail sales data.",
        "Explanation of why it may be important": "Consumer spending signal, predicts retail stock trends (e.g., TGT).",
        "Exchange": "Other (FRED)",
        "Type": "Monthly",
        "Lag number": 14-21,
        "Source": "FRED",
        "Potential Lead": "5-15 days"
    },
    
    # Non-Yahoo Indicators (~Manufacturing & PMI Surveys ~5-20 Days)
    {
        "Symbol": "ISM_MFG_PMI",
        "Title": "ISM Manufacturing PMI",
        "Explanation of what this": "Monthly Purchasing Managers' Index for U.S. manufacturing.",
        "Explanation of why it may be important": "Manufacturing activity signal, predicts industrial stock trends (e.g., CAT).",
        "Exchange": "Other (ISM)",
        "Type": "Monthly",
        "Lag number": 7-14,
        "Source": "Other (ISM ~external fetch)",
        "Potential Lead": "5-20 days"
    },
    {
        "Symbol": "ISM_SRV_PMI",
        "Title": "ISM Services PMI",
        "Explanation of what this": "Monthly Purchasing Managers' Index for U.S. services.",
        "Explanation of why it may be important": "Services activity signal, predicts service stock trends (e.g., SBUX).",
        "Exchange": "Other (ISM)",
        "Type": "Monthly",
        "Lag number": 7-14,
        "Source": "Other (ISM ~external fetch)",
        "Potential Lead": "5-20 days"
    },
    {
        "Symbol": "MARKIT_MFG_PMI",
        "Title": "Markit U.S. Manufacturing PMI",
        "Explanation of what this": "Monthly Purchasing Managers' Index for U.S. manufacturing by Markit.",
        "Explanation of why it may be important": "Manufacturing signal, predicts industrial stock performance.",
        "Exchange": "Other (Markit)",
        "Type": "Monthly",
        "Lag number": 7-14,
        "Source": "Other (Markit ~external fetch)",
        "Potential Lead": "5-20 days"
    },
    
    # Non-Yahoo Indicators (~Fed Liquidity Indicators ~5-15 Days)
    {
        "Symbol": "WALCL",
        "Title": "Fed Balance Sheet Size",
        "Explanation of what this": "Weekly total assets of the Federal Reserve balance sheet.",
        "Explanation of why it may be important": "Liquidity signal, predicts financial market conditions and stock trends.",
        "Exchange": "Other (FRED)",
        "Type": "Weekly",
        "Lag number": 7,
        "Source": "FRED",
        "Potential Lead": "5-15 days"
    },
    
    # Non-Yahoo Indicators (~Alternative Economic Indicators ~5-15 Days)
    {
        "Symbol": "RPI",
        "Title": "Restaurant Performance Index",
        "Explanation of what this": "Monthly index of U.S. restaurant industry performance.",
        "Explanation of why it may be important": "Discretionary spending signal, predicts consumer stock trends (e.g., MCD).",
        "Exchange": "Other (NRA)",
        "Type": "Monthly",
        "Lag number": 7-14,
        "Source": "Other (NRA ~external fetch)",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "HOTEL_OCC",
        "Title": "Hotel Occupancy Rates",
        "Explanation of what this": "Weekly U.S. hotel occupancy rates from STR reports.",
        "Explanation of why it may be important": "Economic strength signal, predicts travel stock trends (e.g., MAR).",
        "Exchange": "Other (STR)",
        "Type": "Weekly",
        "Lag number": 7,
        "Source": "Other (STR ~external fetch)",
        "Potential Lead": "5-15 days"
    },
    
    # Non-Yahoo Indicators (~Subtle Consumer Stress Indicators ~5-15 Days)
    {
        "Symbol": "SUBPRIME_DELQ",
        "Title": "Subprime Auto Loan Delinquencies",
        "Explanation of what this": "Quarterly data on U.S. subprime auto loan delinquencies.",
        "Explanation of why it may be important": "Consumer stress signal, rising delinquencies predict weakening consumer stocks (e.g., F).",
        "Exchange": "Other (Experian)",
        "Type": "Quarterly",
        "Lag number": 30-90,
        "Source": "Other (Experian ~external fetch)",
        "Potential Lead": "5-15 days"
    },
    {
        "Symbol": "TOTALSL",
        "Title": "Consumer Credit Outstanding",
        "Explanation of what this": "Monthly total U.S. consumer credit outstanding (Fed G.19).",
        "Explanation of why it may be important": "Consumer borrowing signal, predicts spending and stock trends.",
        "Exchange": "Other (FRED)",
        "Type": "Monthly",
        "Lag number": 30,
        "Source": "FRED",
        "Potential Lead": "5-15 days"
    }
]