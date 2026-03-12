import pandas as pd

def verify():
    df = pd.read_excel("dados-tratados.xlsx")
    
    # Logic from dashboard.py
    df["Venda_Valor_Diario"] = df["Venda_Media_Diaria"] * df["Custo_Unitario"]
    
    # Section 1: Capital Distribution
    # Note: df_f is the filtered DF. Let's assume no filters for this check.
    tabela_cat = df.groupby("Categoria").agg(
        Venda_Media_Unidades=("Venda_Media_Diaria", "sum"),
        Venda_Total_R=("Venda_Valor_Diario", "sum"),
    )
    
    print("--- Section 1: Category Aggregates ---")
    print(tabela_cat)
    
    # Section 2: Rupture Risk
    # This view shows individual items.
    # The user asks if the SUM of these items matches.
    # To check consistency, let's take all items of a category and sum their sales.
    
    for cat in df["Categoria"].unique():
        sum_units = df[df["Categoria"] == cat]["Venda_Media_Diaria"].sum()
        sum_value = df[df["Categoria"] == cat]["Venda_Valor_Diario"].sum()
        
        cat_agg = tabela_cat.loc[cat]
        
        match_units = abs(sum_units - cat_agg["Venda_Media_Unidades"]) < 1e-5
        match_value = abs(sum_value - cat_agg["Venda_Total_R"]) < 1e-5
        
        print(f"\nCategory: {cat}")
        print(f"  Units: Calculated Sum={sum_units:.2f}, Agg Table={cat_agg['Venda_Media_Unidades']:.2f} -> Match: {match_units}")
        print(f"  Value: Calculated Sum={sum_value:.2f}, Agg Table={cat_agg['Venda_Total_R']:.2f} -> Match: {match_value}")

if __name__ == "__main__":
    verify()
