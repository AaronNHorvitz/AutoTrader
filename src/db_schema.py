# src/db_schema.py

DATABASES = {
    "assets.db": [
        """
        CREATE TABLE IF NOT EXISTS asset_metadata (
            asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT UNIQUE,
            name TEXT,
            exchange TEXT,
            asset_type TEXT,
            is_active INTEGER,
            date_added TEXT,
            date_removed TEXT,
            fetched_at TEXT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS asset_dividends (
            dividend_id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER,
            symbol TEXT,
            ex_date TEXT,
            record_date TEXT,
            pay_date TEXT,
            amount REAL,
            currency TEXT,
            dividend_type TEXT,
            source TEXT,
            fetched_at TEXT,
            FOREIGN KEY (asset_id) REFERENCES asset_metadata(asset_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS corporate_actions (
            action_id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER,
            symbol TEXT,
            action_type TEXT,
            action_description TEXT,
            action_date TEXT,
            ratio REAL,
            cash_value REAL,
            notes TEXT,
            fetched_at TEXT,
            FOREIGN KEY (asset_id) REFERENCES asset_metadata(asset_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS asset_prices (
            price_id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            adjusted_close REAL,
            volume INTEGER,
            fetched_at TEXT,
            FOREIGN KEY (asset_id) REFERENCES asset_metadata(asset_id)
        );
        """
    ],

    "portfolio_management.db": [
        """
        CREATE TABLE IF NOT EXISTS asset_holdings (
            holding_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER,
            asset_id INTEGER,
            date TEXT,
            quantity REAL,
            avg_cost REAL,
            last_updated TEXT,
            FOREIGN KEY (account_id) REFERENCES record_of_accounts(account_id),
            FOREIGN KEY (asset_id) REFERENCES asset_metadata(asset_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER,
            asset_id INTEGER,
            transaction_type TEXT,
            quantity REAL,
            price REAL,
            fees REAL,
            timestamp TEXT,
            FOREIGN KEY (account_id) REFERENCES record_of_accounts(account_id),
            FOREIGN KEY (asset_id) REFERENCES asset_metadata(asset_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS kpi_tracker (
            kpi_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER,
            kpi_date TEXT,
            total_return REAL,
            daily_return REAL,
            win_rate REAL,
            profit_factor REAL,
            max_drawdown REAL,
            sharpe_ratio REAL,
            alpha REAL,
            beta REAL,
            volatility REAL,
            trading_days INTEGER,
            timestamp TEXT,
            FOREIGN KEY (account_id) REFERENCES record_of_accounts(account_id)
        );
        """
    ],

    "accounting.db": [
        """
        CREATE TABLE IF NOT EXISTS record_of_accounts (
            account_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT,
            account_type TEXT,
            owner TEXT,
            status TEXT,
            date_opened TEXT,
            date_closed TEXT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS account_balances (
            balance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER,
            date TEXT,
            cash_available REAL,
            total_cash REAL,
            total_assets_value REAL,
            total_equity REAL,
            liabilities REAL,
            FOREIGN KEY (account_id) REFERENCES record_of_accounts(account_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS record_of_cash_flows (
            cash_flow_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER,
            date TEXT,
            cash_addition REAL,
            cash_withdrawal REAL,
            fees REAL,
            note TEXT,
            FOREIGN KEY (account_id) REFERENCES record_of_accounts(account_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS tax_transactions (
            tax_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER,
            transaction_id INTEGER,
            realized_gain REAL,
            tax_liability REAL,
            tax_paid REAL,
            tax_year INTEGER,
            date_recorded TEXT,
            FOREIGN KEY (account_id) REFERENCES record_of_accounts(account_id),
            FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
        );
        """
    ],

    "modeling.db": [
        """
        CREATE TABLE IF NOT EXISTS model_forecasts (
            forecast_id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT,
            asset_id INTEGER,
            forecast_date TEXT,
            predicted_return REAL,
            confidence REAL,
            horizon_days INTEGER,
            model_version TEXT,
            FOREIGN KEY (asset_id) REFERENCES asset_metadata(asset_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS actual_forecasts (
            actual_id INTEGER PRIMARY KEY AUTOINCREMENT,
            forecast_id INTEGER,
            actual_return REAL,
            comparison_date TEXT,
            FOREIGN KEY (forecast_id) REFERENCES model_forecasts(forecast_id)
        );
        """
    ],

    "exogenous.db": [
        """
        CREATE TABLE IF NOT EXISTS exogenous_metadata (
            exog_id INTEGER PRIMARY KEY AUTOINCREMENT,
            exog_symbol TEXT UNIQUE,
            exog_title TEXT,
            explanation_description TEXT,
            explanation_importance TEXT,
            source TEXT,
            frequency TEXT,
            units TEXT,
            lag REAL,
            in_use INTEGER,
            date_added TEXT,
            last_fetch TEXT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS exogenous_vals (
            exog_vals_id INTEGER PRIMARY KEY AUTOINCREMENT,
            exog_id INTEGER,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            adjusted_close REAL,
            fetched_at TEXT,
            FOREIGN KEY (exog_id) REFERENCES exogenous_metadata(exog_id)
        );
        """
    ],

    "db_change_log.db": [
        """
        CREATE TABLE IF NOT EXISTS change_log (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_name TEXT,
            change_type TEXT,
            change_detail TEXT,
            changed_at TEXT,
            user TEXT,
            db_name TEXT
        );
        """
    ]
}
