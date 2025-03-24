import streamlit as st
import pandas as pd
import numpy as np
import random
import os
import json
import time
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import threading

class OptimizationManager:
    """Gerencia as 5000 otimizações de estratégias de trading, farming, staking e mineração"""
    
    def __init__(self):
        """Inicializa o gerenciador de otimizações"""
        self.categories = ["trading", "yield_farming", "staking", "mining"]
        self.category_names = {
            "trading": "Trading de Alta Frequência",
            "yield_farming": "Yield Farming",
            "staking": "Staking",
            "mining": "Mineração"
        }
        
        self.strategies = {
            "trading": [],
            "yield_farming": [],
            "staking": [],
            "mining": []
        }
        
        # Status geral do sistema de otimização
        self.active = False
        self.running_thread = None
        self.last_optimization = None
        
        # Estatísticas
        self.total_optimizations = 0
        self.successful_transactions = 0
        self.total_volume_processed = 0
        self.current_profit = 0
        self.projected_profit = 0
        
        # Carrega estratégias
        self._load_strategies()
    
    def _load_strategies(self):
        """Carrega estratégias dos anexos ou mock data para demonstração"""
        # Carregar dos arquivos txt anexados
        attachments_dir = "./attached_assets"
        optimization_files = [
            "Pasted-Para-criar-uma-lista-de-5000-estrat-gias-vi-veis-para-yield-farming-staking-trading-e-minera-o-em-1742618886913.txt",
            "Pasted-Para-criar-uma-lista-de-5000-estrat-gias-vi-veis-para-yield-farming-staking-trading-e-minera-o-em-1742619121060.txt"
        ]
        
        strategies_found = []
        
        # Tenta carregar dos arquivos anexados
        try:
            for file_name in optimization_files:
                file_path = os.path.join(attachments_dir, file_name)
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Extrair estratégias do conteúdo
                        # Formatar cada linha como uma estratégia separada
                        lines = content.split('\n')
                        for line in lines:
                            if len(line.strip()) > 10:  # Linhas não vazias
                                strategies_found.append(line.strip())
        except Exception as e:
            print(f"Erro ao carregar estratégias dos arquivos: {str(e)}")
        
        # Distribuir estratégias encontradas entre as categorias
        if strategies_found:
            # Distribuir equilibradamente entre as 4 categorias
            strategies_per_category = len(strategies_found) // 4
            remainder = len(strategies_found) % 4
            
            start = 0
            for i, category in enumerate(self.categories):
                extra = 1 if i < remainder else 0
                end = start + strategies_per_category + extra
                
                category_strategies = strategies_found[start:end]
                
                for idx, strategy in enumerate(category_strategies):
                    self.strategies[category].append({
                        "id": f"{category[0].upper()}{idx+1:04d}",
                        "name": strategy if len(strategy) < 100 else strategy[:97] + "...",
                        "description": strategy,
                        "profit_potential": round(random.uniform(0.1, 5.0), 2),
                        "risk_level": random.choice(["low", "medium", "high"]),
                        "complexity": random.choice(["low", "medium", "high"]),
                        "execution_time": random.randint(10, 3600),  # Em segundos
                        "success_rate": round(random.uniform(80, 99.9), 1),
                        "enabled": random.random() > 0.3,  # 70% ativadas por padrão
                        "times_executed": random.randint(0, 1000),
                        "total_profit": round(random.uniform(0, 10000), 2)
                    })
                
                start = end
        
        # Se não encontrou estratégias suficientes, gera mais para completar 5000
        total_strategies = sum(len(v) for v in self.strategies.values())
        
        if total_strategies < 5000:
            remaining = 5000 - total_strategies
            strategies_per_cat = remaining // 4
            
            for category in self.categories:
                current_count = len(self.strategies[category])
                
                for i in range(strategies_per_cat):
                    idx = current_count + i
                    template = self._generate_strategy_template(category)
                    
                    self.strategies[category].append({
                        "id": f"{category[0].upper()}{idx+1:04d}",
                        "name": template["name"],
                        "description": template["description"],
                        "profit_potential": round(random.uniform(0.1, 5.0), 2),
                        "risk_level": random.choice(["low", "medium", "high"]),
                        "complexity": random.choice(["low", "medium", "high"]),
                        "execution_time": random.randint(10, 3600),  # Em segundos
                        "success_rate": round(random.uniform(80, 99.9), 1),
                        "enabled": random.random() > 0.3,  # 70% ativadas por padrão
                        "times_executed": random.randint(0, 1000),
                        "total_profit": round(random.uniform(0, 10000), 2)
                    })
    
    def _generate_strategy_template(self, category):
        """Gera templates para diferentes categorias de estratégias"""
        if category == "trading":
            assets = ["BTC", "ETH", "SOL", "AVAX", "BNB", "XRP", "DOT", "DOGE", "MATIC", "LINK"]
            timeframes = ["1m", "5m", "15m", "30m", "1h", "4h", "1d"]
            indicators = ["RSI", "MACD", "Moving Average", "Bollinger Bands", "Stochastic", "Ichimoku Cloud", "Fibonacci"]
            
            asset1 = random.choice(assets)
            asset2 = random.choice([a for a in assets if a != asset1])
            timeframe = random.choice(timeframes)
            indicator1 = random.choice(indicators)
            indicator2 = random.choice([i for i in indicators if i != indicator1])
            
            strategy_type = random.choice([
                "Arbitragem entre {a1}/{a2} em múltiplas exchanges",
                "Scalping de {a1} com {i1} em timeframe de {tf}",
                "Swing Trading de {a1}/{a2} com cruzamento de {i1} e {i2}",
                "Market making para {a1}/{a2} com spread dinâmico",
                "Triangular arbitragem {a1}/{a2}/{a3} com execução em milissegundos",
                "Grid trading automatizado para {a1} em {tf}",
                "Trading por reversão à média em {a1} usando {i1}",
                "Detecção de flash crashes em {a1} para compras instantâneas",
                "Arbitragem estatística entre {a1} e {a2} com correlação dinâmica",
                "Trading de momentum em {a1} com filtro de volume"
            ])
            
            asset3 = random.choice([a for a in assets if a != asset1 and a != asset2])
            
            name = strategy_type.format(
                a1=asset1, a2=asset2, a3=asset3, 
                i1=indicator1, i2=indicator2, tf=timeframe
            )
            
            return {
                "name": name,
                "description": f"Estratégia de trading que utiliza {indicator1} e {indicator2} para identificar oportunidades de lucro em {asset1}/{asset2} no timeframe de {timeframe}. " + 
                              f"Inclui proteções contra volatilidade extrema e execução multi-threading para velocidade máxima."
            }
            
        elif category == "yield_farming":
            protocols = ["Aave", "Compound", "Curve", "Uniswap", "SushiSwap", "PancakeSwap", "Trader Joe", "Balancer", "Convex", "Yearn"]
            tokens = ["USDC", "USDT", "DAI", "ETH", "WBTC", "AAVE", "CRV", "UNI", "SUSHI", "CAKE"]
            chains = ["Ethereum", "Polygon", "Arbitrum", "Optimism", "Avalanche", "BNB Chain", "Fantom", "Solana", "Base", "zkSync"]
            
            protocol = random.choice(protocols)
            token1 = random.choice(tokens)
            token2 = random.choice([t for t in tokens if t != token1])
            chain = random.choice(chains)
            apy = random.randint(5, 200)
            
            strategy_type = random.choice([
                "Farming de {t1}/{t2} no {p} em {c} com APY de {apy}%",
                "Rotação automática de rewards em {p} para {t1}",
                "Empréstimo de {t1} em {p} para leverage farming",
                "Estratégia de auto-compounding para {t1}/{t2} em {p}",
                "Zap inteligente para pool {t1}/{t2} em {p} na {c}",
                "Loop de empréstimo-farming com {t1} em múltiplos protocolos",
                "Hedging de impermanent loss em pools {t1}/{t2} em {p}",
                "Aproveitamento de incentivos de {t1} em {p} com sinalização on-chain",
                "Meta-farming para tokens {t1} em {c} usando {p}",
                "Balanceamento automático de multi-pools em {p} para máximo APY"
            ])
            
            name = strategy_type.format(
                p=protocol, t1=token1, t2=token2, c=chain, apy=apy
            )
            
            return {
                "name": name,
                "description": f"Estratégia de yield farming que utiliza o protocolo {protocol} na blockchain {chain} para maximizar retornos com os tokens {token1} e {token2}. " + 
                              f"Inclui rotação automática de recompensas e proteção contra impermanent loss."
            }
            
        elif category == "staking":
            assets = ["ETH", "SOL", "ADA", "DOT", "MATIC", "ATOM", "NEAR", "AVAX", "FTM", "ONE"]
            platforms = ["Lido", "Marinade", "Daedalus", "Polkadot.js", "Polygon PoS", "Cosmos Hub", "NEAR Wallet", "Avalanche P-Chain", "Fantom Staking", "Harmony Staking"]
            
            asset = random.choice(assets)
            platform = random.choice(platforms)
            lock_period = random.choice(["flexível", "30 dias", "90 dias", "180 dias", "1 ano", "multi-ano"])
            apy = random.randint(3, 25)
            
            strategy_type = random.choice([
                "Staking de {a} via {p} com período {lp} para APY de {apy}%",
                "Staking líquido de {a} através de {p} com reinvestimento automático",
                "Noding validador de {a} com {p} para maximizar recompensas",
                "Rotação de delegações de {a} entre validadores top em {p}",
                "Compounding automático de rewards de staking de {a} a cada 24h",
                "Multi-chain staking de {a} com diversificação de validadores",
                "Staking com proteção contra slashing para {a} em {p}",
                "Meta-staking de derivativos de staking de {a} para yield extra",
                "Staking com colateralização para {a} mantendo liquidez",
                "Staking institucional de {a} com custódia segura via {p}"
            ])
            
            name = strategy_type.format(
                a=asset, p=platform, lp=lock_period, apy=apy
            )
            
            return {
                "name": name,
                "description": f"Estratégia de staking que permite ganhar aproximadamente {apy}% APY com {asset} através da plataforma {platform}. " + 
                              f"Inclui período de lock de {lock_period} e reinvestimento automático das recompensas."
            }
            
        elif category == "mining":
            coins = ["BTC", "ETH", "RVN", "ERG", "FLUX", "KASPA", "ZEC", "XMR", "ETC", "ALPH"]
            algos = ["SHA-256", "ETHASH", "KAWPOW", "AUTOLYKOS", "ZHASH", "RANDOMX", "EQUIHASH", "PROGPOW", "SCRYPT", "BLAKE3"]
            
            coin = random.choice(coins)
            algo = random.choice(algos)
            hardware = random.choice(["ASIC", "GPU NVIDIA", "GPU AMD", "CPU", "FPGA"])
            pool = random.choice(["NiceHash", "F2Pool", "Poolin", "Binance Pool", "ViaBTC", "2Miners", "HeroMiners", "MiningPoolHub", "FlexPool", "Ethermine"])
            
            strategy_type = random.choice([
                "Mineração de {c} com {h} via {p} usando algoritmo {a}",
                "Mineração com troca automática para {c} mais lucrativa",
                "Multi-algoritmo mining otimizado para {h} com balanceamento dinâmico",
                "Cloud mining de {c} com hashrate distribuído globalmente",
                "Mining de {c} com overclock otimizado para eficiência energética",
                "Mineração com rotação baseada em lucratividade entre {c} e alternativas",
                "Solo mining de {c} com detecção automática de blocos",
                "Mining híbrido de {c} combinando {h} e cloud mining",
                "Mining com PPS+ em {p} para {c} com pagamentos estáveis",
                "Mining institucional de {c} com múltiplos {h} em data center"
            ])
            
            hashrate_unit = "H/s" if hardware == "CPU" else "MH/s" if hardware == "GPU NVIDIA" or hardware == "GPU AMD" else "TH/s" if hardware == "ASIC" else "GH/s"
            hashrate = random.randint(1, 1000)
            
            name = strategy_type.format(
                c=coin, h=hardware, p=pool, a=algo
            )
            
            return {
                "name": name,
                "description": f"Estratégia de mineração que utiliza {hardware} para minerar {coin} via algoritmo {algo} na pool {pool} com hashrate médio de {hashrate} {hashrate_unit}. " + 
                              f"Inclui monitoramento automático de temperatura e ajuste de clock para eficiência máxima."
            }
        
        return {
            "name": f"Estratégia genérica para {category}",
            "description": f"Descrição detalhada da estratégia para {category}"
        }
    
    def get_category_stats(self):
        """Retorna estatísticas por categoria"""
        stats = {}
        
        for category in self.categories:
            strategies = self.strategies[category]
            enabled_count = sum(1 for s in strategies if s["enabled"])
            
            total_profit = sum(s["total_profit"] for s in strategies if s["enabled"])
            avg_success_rate = sum(s["success_rate"] for s in strategies if s["enabled"]) / enabled_count if enabled_count > 0 else 0
            highest_profit = max((s["total_profit"] for s in strategies if s["enabled"]), default=0)
            
            stats[category] = {
                "name": self.category_names[category],
                "total": len(strategies),
                "enabled": enabled_count,
                "disabled": len(strategies) - enabled_count,
                "total_profit": total_profit,
                "avg_success_rate": avg_success_rate,
                "highest_profit": highest_profit,
                "enabled_percentage": round((enabled_count / len(strategies)) * 100, 1) if strategies else 0
            }
        
        return stats
    
    def get_strategies_by_category(self, category, limit=10, offset=0):
        """Retorna estratégias de uma categoria específica, com paginação"""
        if category not in self.categories:
            return []
        
        strategies = self.strategies[category]
        
        # Aplicar paginação
        end = offset + limit
        if end > len(strategies):
            end = len(strategies)
        
        return strategies[offset:end]
    
    def get_total_stats(self):
        """Retorna estatísticas gerais de todas as estratégias"""
        total_strategies = sum(len(self.strategies[cat]) for cat in self.categories)
        enabled_strategies = sum(sum(1 for s in self.strategies[cat] if s["enabled"]) for cat in self.categories)
        
        total_profit = sum(sum(s["total_profit"] for s in self.strategies[cat] if s["enabled"]) for cat in self.categories)
        total_executions = sum(sum(s["times_executed"] for s in self.strategies[cat] if s["enabled"]) for cat in self.categories)
        
        # Calcular estatísticas de risco
        risk_counts = {"low": 0, "medium": 0, "high": 0}
        for cat in self.categories:
            for s in self.strategies[cat]:
                if s["enabled"]:
                    risk_counts[s["risk_level"]] += 1
        
        return {
            "total_strategies": total_strategies,
            "enabled_strategies": enabled_strategies,
            "disabled_strategies": total_strategies - enabled_strategies,
            "total_profit": total_profit,
            "total_executions": total_executions,
            "risk_distribution": risk_counts,
            "enabled_percentage": round((enabled_strategies / total_strategies) * 100, 1) if total_strategies > 0 else 0
        }
    
    def toggle_strategy(self, category, strategy_id, enabled=True):
        """Ativa ou desativa uma estratégia específica"""
        if category not in self.categories:
            return False
        
        for strategy in self.strategies[category]:
            if strategy["id"] == strategy_id:
                strategy["enabled"] = enabled
                return True
        
        return False
    
    def mass_toggle_category(self, category, percentage):
        """Ativa ou desativa um percentual de estratégias em uma categoria"""
        if category not in self.categories:
            return False
        
        strategies = self.strategies[category]
        total = len(strategies)
        target_count = int(total * percentage / 100)
        
        # Resetar todas para desativado
        for strategy in strategies:
            strategy["enabled"] = False
        
        # Ativar o número alvo, selecionando as mais lucrativas primeiro
        sorted_strategies = sorted(strategies, key=lambda s: s["profit_potential"], reverse=True)
        for i in range(min(target_count, total)):
            sorted_strategies[i]["enabled"] = True
        
        return True
    
    def get_strategy_details(self, category, strategy_id):
        """Retorna detalhes de uma estratégia específica"""
        if category not in self.categories:
            return None
        
        for strategy in self.strategies[category]:
            if strategy["id"] == strategy_id:
                return strategy
        
        return None
    
    def search_strategies(self, query, limit=20):
        """Pesquisa estratégias em todas as categorias"""
        if not query or len(query) < 3:
            return []
        
        query = query.lower()
        results = []
        
        for category in self.categories:
            for strategy in self.strategies[category]:
                if (query in strategy["name"].lower() or 
                    query in strategy["description"].lower()):
                    strategy_copy = strategy.copy()
                    strategy_copy["category"] = category
                    strategy_copy["category_name"] = self.category_names[category]
                    results.append(strategy_copy)
                    
                    if len(results) >= limit:
                        return results
        
        return results
    
    def generate_optimization_report(self):
        """Gera um relatório de otimizações ativas"""
        stats = self.get_total_stats()
        category_stats = self.get_category_stats()
        
        # Top 3 estratégias mais lucrativas por categoria
        top_strategies = {}
        for category in self.categories:
            sorted_strats = sorted(
                [s for s in self.strategies[category] if s["enabled"]], 
                key=lambda s: s["total_profit"], 
                reverse=True
            )
            top_strategies[category] = sorted_strats[:3]
        
        return {
            "timestamp": datetime.now(),
            "overall_stats": stats,
            "category_stats": category_stats,
            "top_strategies": top_strategies,
            "optimization_status": "active" if self.active else "inactive",
            "last_optimization": self.last_optimization,
            "total_optimizations": self.total_optimizations
        }

# Singleton para uso global
_optimization_manager = None

def get_optimization_manager():
    """Retorna uma instância do gerenciador de otimizações"""
    global _optimization_manager
    if _optimization_manager is None:
        _optimization_manager = OptimizationManager()
    return _optimization_manager

def render_page():
    st.header("Hub de Otimizações Massivas")
    
    st.markdown("""
    ### Sistema de 5000 Estratégias Inteligentes
    
    Este módulo implementa 5000 estratégias avançadas para maximizar lucros em:
    
    - **Trading de Alta Frequência**: Estratégias de arbitragem, scalping e outros
    - **Yield Farming**: Estratégias de DeFi com compounding automático
    - **Staking**: Estratégias de staking otimizadas por blockchain
    - **Mineração**: Estratégias de mineração multi-algoritmo
    """)
    
    # Obter instância do otimizador
    manager = get_optimization_manager()
    
    # Estatísticas gerais
    total_stats = manager.get_total_stats()
    category_stats = manager.get_category_stats()
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total de Estratégias", 
            f"{total_stats['total_strategies']:,}",
            f"{total_stats['enabled_percentage']}% Ativas"
        )
    
    with col2:
        st.metric(
            "Estratégias Ativas", 
            f"{total_stats['enabled_strategies']:,}"
        )
    
    with col3:
        st.metric(
            "Lucro Total", 
            f"${total_stats['total_profit']:,.2f}"
        )
    
    with col4:
        st.metric(
            "Execuções Totais", 
            f"{total_stats['total_executions']:,}"
        )
    
    # Distribuição de estratégias
    st.subheader("Distribuição de Estratégias")
    
    # Criar dados para gráfico
    categories = [category_stats[cat]["name"] for cat in manager.categories]
    enabled_counts = [category_stats[cat]["enabled"] for cat in manager.categories]
    disabled_counts = [category_stats[cat]["disabled"] for cat in manager.categories]
    
    # Criar gráfico de barras agrupadas
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=categories,
        y=enabled_counts,
        name="Ativas",
        marker_color="green"
    ))
    
    fig.add_trace(go.Bar(
        x=categories,
        y=disabled_counts,
        name="Inativas",
        marker_color="red"
    ))
    
    fig.update_layout(
        barmode="stack",
        title="Estratégias Ativas vs. Inativas por Categoria",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Distribuição de risco
    risk_data = total_stats["risk_distribution"]
    
    risk_fig = px.pie(
        values=list(risk_data.values()),
        names=[r.capitalize() for r in risk_data.keys()],
        title="Distribuição de Risco das Estratégias Ativas",
        color_discrete_map={"Low": "green", "Medium": "orange", "High": "red"}
    )
    
    risk_fig.update_traces(textposition='inside', textinfo='percent+label')
    
    st.plotly_chart(risk_fig, use_container_width=True)
    
    # Abas para cada categoria
    tabs = st.tabs([category_stats[cat]["name"] for cat in manager.categories])
    
    for i, category in enumerate(manager.categories):
        with tabs[i]:
            cat_stats = category_stats[category]
            
            st.subheader(f"Estratégias de {cat_stats['name']}")
            
            # Métricas da categoria
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Total de Estratégias", 
                    f"{cat_stats['total']:,}",
                    f"{cat_stats['enabled_percentage']}% Ativas"
                )
            
            with col2:
                st.metric(
                    "Lucro Total", 
                    f"${cat_stats['total_profit']:,.2f}"
                )
            
            with col3:
                st.metric(
                    "Taxa de Sucesso Média", 
                    f"{cat_stats['avg_success_rate']:.2f}%"
                )
            
            # Controles de ativação em massa
            st.subheader("Controle de Ativação em Massa")
            
            percentage = st.slider(
                "Percentual de Estratégias Ativas", 
                min_value=0, 
                max_value=100, 
                value=int(cat_stats["enabled_percentage"]), 
                key=f"slider_{category}"
            )
            
            if st.button("Aplicar", key=f"apply_{category}"):
                if manager.mass_toggle_category(category, percentage):
                    st.success(f"Configuração aplicada. {percentage}% das estratégias de {cat_stats['name']} estão ativas.")
                    st.rerun()
                else:
                    st.error("Erro ao aplicar configuração.")
            
            # Tabela de estratégias
            st.subheader("Lista de Estratégias")
            
            # Configurações de paginação
            strategies_per_page = 10
            total_pages = (cat_stats["total"] + strategies_per_page - 1) // strategies_per_page
            
            col1, col2 = st.columns([3, 1])
            with col1:
                page = st.number_input(
                    "Página", 
                    min_value=1, 
                    max_value=max(total_pages, 1), 
                    value=1, 
                    key=f"page_{category}"
                )
            
            with col2:
                st.text(f"Total: {total_pages} páginas")
            
            # Calcular offset para paginação
            offset = (page - 1) * strategies_per_page
            
            # Obter estratégias para a página atual
            strategies = manager.get_strategies_by_category(
                category, 
                limit=strategies_per_page, 
                offset=offset
            )
            
            # Criar DataFrame para exibição
            if strategies:
                df_data = []
                for s in strategies:
                    df_data.append({
                        "ID": s["id"],
                        "Nome": s["name"],
                        "Potencial de Lucro": f"{s['profit_potential']}%",
                        "Risco": s["risk_level"].capitalize(),
                        "Complexidade": s["complexity"].capitalize(),
                        "Taxa de Sucesso": f"{s['success_rate']}%",
                        "Status": "Ativa" if s["enabled"] else "Inativa",
                        "Execuções": s["times_executed"],
                        "Lucro Total": f"${s['total_profit']:,.2f}"
                    })
                
                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True)
                
                # Seletor de estratégia para detalhes
                selected_id = st.selectbox(
                    "Selecione uma estratégia para ver detalhes", 
                    [s["id"] for s in strategies],
                    format_func=lambda x: next((s["name"] for s in strategies if s["id"] == x), x),
                    key=f"select_{category}"
                )
                
                if selected_id:
                    selected_strategy = manager.get_strategy_details(category, selected_id)
                    
                    if selected_strategy:
                        st.subheader(f"Detalhes da Estratégia {selected_strategy['id']}")
                        
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"### {selected_strategy['name']}")
                            st.markdown(f"**Descrição:** {selected_strategy['description']}")
                            
                            st.markdown("#### Métricas")
                            st.markdown(f"- **Potencial de Lucro:** {selected_strategy['profit_potential']}%")
                            st.markdown(f"- **Nível de Risco:** {selected_strategy['risk_level'].capitalize()}")
                            st.markdown(f"- **Complexidade:** {selected_strategy['complexity'].capitalize()}")
                            st.markdown(f"- **Taxa de Sucesso:** {selected_strategy['success_rate']}%")
                            st.markdown(f"- **Tempo de Execução:** {selected_strategy['execution_time']} segundos")
                            st.markdown(f"- **Vezes Executada:** {selected_strategy['times_executed']:,}")
                            st.markdown(f"- **Lucro Total:** ${selected_strategy['total_profit']:,.2f}")
                        
                        with col2:
                            # Status atual
                            st.markdown("#### Status")
                            st.markdown(f"**Status Atual:** {'Ativa' if selected_strategy['enabled'] else 'Inativa'}")
                            
                            # Botão para alternar status
                            if selected_strategy['enabled']:
                                if st.button("Desativar Estratégia", key=f"disable_{selected_id}"):
                                    if manager.toggle_strategy(category, selected_id, False):
                                        st.success(f"Estratégia {selected_id} desativada.")
                                        st.rerun()
                                    else:
                                        st.error("Erro ao desativar estratégia.")
                            else:
                                if st.button("Ativar Estratégia", key=f"enable_{selected_id}", type="primary"):
                                    if manager.toggle_strategy(category, selected_id, True):
                                        st.success(f"Estratégia {selected_id} ativada.")
                                        st.rerun()
                                    else:
                                        st.error("Erro ao ativar estratégia.")
                            
                            # Gráfico de pizza para composição de risco/retorno
                            fig = go.Figure(data=[go.Pie(
                                labels=["Risco", "Retorno", "Complexidade"],
                                values=[
                                    {"low": 1, "medium": 2, "high": 3}[selected_strategy["risk_level"]],
                                    selected_strategy["profit_potential"],
                                    {"low": 1, "medium": 2, "high": 3}[selected_strategy["complexity"]]
                                ],
                                hole=.3
                            )])
                            
                            fig.update_layout(title="Perfil da Estratégia")
                            st.plotly_chart(fig, use_container_width=True)
                        
                        # Simulação de execução
                        st.subheader("Simulação de Execução")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            capital = st.number_input("Capital a Investir ($)", min_value=1.0, value=1000.0)
                        
                        with col2:
                            repetitions = st.number_input("Repetições", min_value=1, max_value=10000, value=1)
                        
                        with col3:
                            # Taxa de sucesso ajustada para simulação
                            success_rate_adj = st.slider(
                                "Taxa de Sucesso (%)", 
                                min_value=0.0, 
                                max_value=100.0, 
                                value=float(selected_strategy["success_rate"])
                            )
                        
                        # Calcular resultado da simulação
                        if st.button("Simular Execução", type="primary"):
                            # Simulação
                            successful_ops = 0
                            failed_ops = 0
                            
                            total_profit = 0
                            execution_seconds = 0
                            
                            for _ in range(repetitions):
                                # Simular sucesso baseado na taxa
                                if random.random() * 100 < success_rate_adj:
                                    # Operação bem-sucedida
                                    successful_ops += 1
                                    profit = capital * (selected_strategy["profit_potential"] / 100)
                                    total_profit += profit
                                else:
                                    # Operação falhou
                                    failed_ops += 1
                                    # Perda aleatória de 0 a 50% do potencial de lucro
                                    loss = capital * (selected_strategy["profit_potential"] / 100) * (random.random() * 0.5)
                                    total_profit -= loss
                                
                                # Adicionar tempo de execução
                                execution_seconds += selected_strategy["execution_time"]
                            
                            # Exibir resultados
                            st.success("Simulação concluída!")
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("Operações Bem-sucedidas", successful_ops)
                            
                            with col2:
                                st.metric("Operações Falhas", failed_ops)
                            
                            with col3:
                                hours = execution_seconds // 3600
                                minutes = (execution_seconds % 3600) // 60
                                seconds = execution_seconds % 60
                                
                                time_str = ""
                                if hours > 0:
                                    time_str += f"{hours}h "
                                if minutes > 0 or hours > 0:
                                    time_str += f"{minutes}m "
                                time_str += f"{seconds}s"
                                
                                st.metric("Tempo Total", time_str)
                            
                            # Resultado financeiro
                            st.metric(
                                "Resultado Financeiro", 
                                f"${total_profit:,.2f}", 
                                f"{(total_profit / capital) * 100:.2f}% do capital inicial"
                            )
                            
                            # Gráfico de operações
                            st.subheader("Distribuição de Operações")
                            
                            fig = go.Figure(data=[go.Pie(
                                labels=["Bem-sucedidas", "Falhas"],
                                values=[successful_ops, failed_ops],
                                hole=.3,
                                marker_colors=["green", "red"]
                            )])
                            
                            st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(f"Não há estratégias disponíveis para {category_stats[category]['name']}.")
    
    # Seção de pesquisa
    st.header("Pesquisa de Estratégias")
    
    query = st.text_input("Pesquisar estratégias", placeholder="Digite ao menos 3 caracteres...")
    
    if query and len(query) >= 3:
        results = manager.search_strategies(query)
        
        if results:
            st.success(f"Encontradas {len(results)} estratégias para '{query}'")
            
            # Exibir resultados em tabela
            df_data = []
            for s in results:
                df_data.append({
                    "ID": s["id"],
                    "Nome": s["name"],
                    "Categoria": s["category_name"],
                    "Potencial de Lucro": f"{s['profit_potential']}%",
                    "Risco": s["risk_level"].capitalize(),
                    "Taxa de Sucesso": f"{s['success_rate']}%",
                    "Status": "Ativa" if s["enabled"] else "Inativa"
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info(f"Nenhuma estratégia encontrada para '{query}'")
    
    # Relatório de otimização
    st.header("Relatório de Otimização")
    
    if st.button("Gerar Relatório de Otimização"):
        report = manager.generate_optimization_report()
        
        st.subheader("Relatório Gerado")
        st.markdown(f"**Data/Hora:** {report['timestamp'].strftime('%d/%m/%Y %H:%M:%S')}")
        st.markdown(f"**Status das Otimizações:** {'Ativo' if report['optimization_status'] == 'active' else 'Inativo'}")
        
        # Resumo de estatísticas
        st.subheader("Resumo de Estatísticas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total de Estratégias", f"{report['overall_stats']['total_strategies']:,}")
            st.metric("Estratégias Ativas", f"{report['overall_stats']['enabled_strategies']:,}")
            st.metric("Percentual Ativo", f"{report['overall_stats']['enabled_percentage']}%")
        
        with col2:
            st.metric("Lucro Total", f"${report['overall_stats']['total_profit']:,.2f}")
            st.metric("Execuções Totais", f"{report['overall_stats']['total_executions']:,}")
        
        # Top estratégias por categoria
        st.subheader("Top Estratégias por Categoria")
        
        for category in manager.categories:
            cat_name = report['category_stats'][category]['name']
            top_strats = report['top_strategies'][category]
            
            if top_strats:
                st.markdown(f"#### {cat_name}")
                
                for i, strat in enumerate(top_strats):
                    st.markdown(f"**{i+1}.** {strat['name']}")
                    st.markdown(f"   Lucro: ${strat['total_profit']:,.2f} | Taxa de Sucesso: {strat['success_rate']}% | Execuções: {strat['times_executed']:,}")
            else:
                st.markdown(f"#### {cat_name}")
                st.info(f"Não há estratégias ativas para {cat_name}")
        
        # Gráfico de distribuição de lucro por categoria
        st.subheader("Distribuição de Lucro por Categoria")
        
        profit_data = {
            cat: report['category_stats'][cat]['total_profit'] 
            for cat in manager.categories
        }
        
        fig = px.pie(
            names=[report['category_stats'][cat]['name'] for cat in profit_data.keys()],
            values=list(profit_data.values()),
            title="Distribuição de Lucro Total por Categoria"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Aviso legal
    st.warning("""
    **AVISO:** O sistema de 5000 estratégias de otimização massiva está em modo de demonstração. 
    Em um ambiente de produção, estas estratégias seriam executadas automaticamente com 
    base nas configurações ativas, buscando o máximo lucro em todas as operações.
    """)