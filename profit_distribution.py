import streamlit as st
import pandas as pd
import numpy as np
import time
import threading
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

class ProfitDistributor:
    """Sistema de distribuição automática de lucros"""
    
    def __init__(self):
        """Inicializa o distribuidor de lucros"""
        self.btc_wallet = "16LaAQi8cfyYSTzB3cDqsSkFRJGDbN1cLS"
        self.distribution_rules = {
            "wallet_btc": 50.0,  # 50% para a carteira BTC
            "reinvestment": 20.0,  # 20% para reinvestimento
            "operational": 15.0,  # 15% para taxas e servidor
            "mining_fees": 5.0,  # 5% para taxas de mineração
            "liquidity_pool": 10.0  # 10% para pool de liquidez
        }
        
        # Detalhamento do reinvestimento (dentro dos 20%)
        self.reinvestment_allocation = {
            "yield_farming": 35.0,  # 35% dos 20% = 7% do total
            "staking": 30.0,  # 30% dos 20% = 6% do total
            "trading": 25.0,  # 25% dos 20% = 5% do total
            "airdrops": 10.0  # 10% dos 20% = 2% do total
        }
        
        # Histórico de distribuições
        self.distribution_history = []
        
        # Controle do thread de distribuição
        self.running = False
        self.distribution_thread = None
        self.last_distribution = None
        self.distribution_interval = 3600  # 1 hora em segundos
        
        # Estatísticas
        self.total_distributed = 0.0
        self.total_to_wallet = 0.0
        self.total_reinvested = 0.0
        self.total_operational = 0.0
        self.total_mining_fees = 0.0
        self.total_liquidity = 0.0
        
        # Status de transações recentes
        self.recent_transactions = []
    
    def start_auto_distribution(self):
        """Inicia a distribuição automática de lucros"""
        if self.running:
            return "A distribuição automática já está em execução"
        
        self.running = True
        self.distribution_thread = threading.Thread(target=self._distribution_loop, daemon=True)
        self.distribution_thread.start()
        
        return "Distribuição automática de lucros iniciada com sucesso"
    
    def stop_auto_distribution(self):
        """Para a distribuição automática de lucros"""
        if not self.running:
            return "A distribuição automática já está parada"
        
        self.running = False
        if self.distribution_thread:
            self.distribution_thread.join(timeout=2.0)
        
        return "Distribuição automática de lucros parada com sucesso"
    
    def _distribution_loop(self):
        """Loop de distribuição automática a cada hora"""
        while self.running:
            # Simula a geração de lucro durante o período
            profit = self._simulate_profit_generation()
            
            # Realiza a distribuição
            distribution = self.distribute_profit(profit)
            
            # Registra a distribuição
            self.last_distribution = datetime.now()
            self.distribution_history.append({
                "timestamp": self.last_distribution,
                "profit": profit,
                "distribution": distribution
            })
            
            # Limita o histórico a 1000 entradas
            if len(self.distribution_history) > 1000:
                self.distribution_history = self.distribution_history[-1000:]
            
            # Espera até a próxima hora
            time.sleep(self.distribution_interval)
    
    def _simulate_profit_generation(self):
        """Simula a geração de lucro durante o período"""
        # Simulação: entre $50 e $10,000 por hora
        return round(random.uniform(50, 10000), 2)
    
    def distribute_profit(self, profit):
        """Distribui o lucro de acordo com as regras estabelecidas"""
        # Calcula os valores para cada categoria
        distribution = {}
        
        # 50% para a carteira BTC
        wallet_amount = profit * (self.distribution_rules["wallet_btc"] / 100)
        distribution["wallet_btc"] = wallet_amount
        self.total_to_wallet += wallet_amount
        
        # Adiciona transação recente para a carteira BTC
        self.recent_transactions.append({
            "timestamp": datetime.now(),
            "type": "BTC Transfer",
            "amount": wallet_amount,
            "address": self.btc_wallet,
            "status": "Completed",
            "tx_hash": self._generate_fake_tx_hash()
        })
        
        # 20% para reinvestimento
        reinvestment_amount = profit * (self.distribution_rules["reinvestment"] / 100)
        distribution["reinvestment"] = reinvestment_amount
        self.total_reinvested += reinvestment_amount
        
        # Detalhe do reinvestimento
        distribution["reinvestment_detail"] = {}
        for category, percentage in self.reinvestment_allocation.items():
            category_amount = reinvestment_amount * (percentage / 100)
            distribution["reinvestment_detail"][category] = category_amount
            
            # Adiciona transação recente para reinvestimento
            self.recent_transactions.append({
                "timestamp": datetime.now(),
                "type": f"Reinvestment ({category})",
                "amount": category_amount,
                "status": "Processed"
            })
        
        # 15% para operacional
        operational_amount = profit * (self.distribution_rules["operational"] / 100)
        distribution["operational"] = operational_amount
        self.total_operational += operational_amount
        
        # Adiciona transação recente para operacional
        self.recent_transactions.append({
            "timestamp": datetime.now(),
            "type": "Operational Reserve",
            "amount": operational_amount,
            "status": "Reserved"
        })
        
        # 5% para taxas de mineração
        mining_fees_amount = profit * (self.distribution_rules["mining_fees"] / 100)
        distribution["mining_fees"] = mining_fees_amount
        self.total_mining_fees += mining_fees_amount
        
        # Adiciona transação recente para taxas de mineração
        self.recent_transactions.append({
            "timestamp": datetime.now(),
            "type": "Mining Fees",
            "amount": mining_fees_amount,
            "status": "Allocated"
        })
        
        # 10% para pool de liquidez
        liquidity_amount = profit * (self.distribution_rules["liquidity_pool"] / 100)
        distribution["liquidity_pool"] = liquidity_amount
        self.total_liquidity += liquidity_amount
        
        # Adiciona transação recente para pool de liquidez
        self.recent_transactions.append({
            "timestamp": datetime.now(),
            "type": "Liquidity Pool (QuickTrust S.A.)",
            "amount": liquidity_amount,
            "status": "Added to Pool"
        })
        
        # Atualiza total distribuído
        self.total_distributed += profit
        
        # Limita as transações recentes a 100
        if len(self.recent_transactions) > 100:
            self.recent_transactions = self.recent_transactions[-100:]
        
        return distribution
    
    def _generate_fake_tx_hash(self):
        """Gera um hash de transação fake para simulação"""
        return ''.join(random.choice('0123456789abcdef') for _ in range(64))
    
    def get_distribution_summary(self):
        """Retorna um resumo das distribuições realizadas"""
        return {
            "total_distributed": self.total_distributed,
            "total_to_wallet": self.total_to_wallet,
            "total_reinvested": self.total_reinvested,
            "total_operational": self.total_operational,
            "total_mining_fees": self.total_mining_fees,
            "total_liquidity": self.total_liquidity,
            "btc_wallet": self.btc_wallet,
            "last_distribution": self.last_distribution,
            "distribution_count": len(self.distribution_history)
        }
    
    def get_recent_transactions(self, limit=10):
        """Retorna as transações mais recentes"""
        return self.recent_transactions[-limit:] if self.recent_transactions else []
    
    def get_distribution_history(self, days=7):
        """Retorna o histórico de distribuições para o período especificado"""
        cutoff = datetime.now() - timedelta(days=days)
        return [d for d in self.distribution_history if d["timestamp"] > cutoff]
    
    def manual_distribute(self, profit):
        """Realiza uma distribuição manual de lucro"""
        distribution = self.distribute_profit(profit)
        
        # Registra a distribuição manual
        self.last_distribution = datetime.now()
        self.distribution_history.append({
            "timestamp": self.last_distribution,
            "profit": profit,
            "distribution": distribution,
            "type": "manual"
        })
        
        return distribution

# Singleton para uso global
_profit_distributor = None

def get_profit_distributor():
    """Retorna uma instância do distribuidor de lucros"""
    global _profit_distributor
    if _profit_distributor is None:
        _profit_distributor = ProfitDistributor()
    return _profit_distributor

def render_page():
    st.header("Sistema de Distribuição de Lucros")
    
    st.markdown("""
    ### Distribuição Automática e Transparente
    
    Este módulo gerencia a distribuição automática de lucros do sistema, de acordo com regras 
    pré-estabelecidas para garantir a sustentabilidade do projeto e maximizar os retornos.
    
    **Distribuição de Lucros:**
    
    - **50%** enviado para a carteira BTC a cada hora
    - **20%** reinvestido (yield farming, staking, trading, airdrops)
    - **15%** reservado para taxas de gas e custos operacionais
    - **5%** alocado para taxas de mineração em nuvem multi-moedas
    - **10%** destinado à pool de liquidez e projeto DeFi do Grupo QuickTrust S.A.
    """)
    
    # Obter instância do distribuidor
    distributor = get_profit_distributor()
    
    # Status do distribuidor
    status_running = distributor.running
    
    # Controles de início/parada da distribuição automática
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Iniciar Distribuição Automática", type="primary", disabled=status_running):
            result = distributor.start_auto_distribution()
            st.success(result)
            st.rerun()
    
    with col2:
        if st.button("Parar Distribuição Automática", disabled=not status_running):
            result = distributor.stop_auto_distribution()
            st.success(result)
            st.rerun()
    
    # Resumo de distribuição
    summary = distributor.get_distribution_summary()
    
    st.subheader("Resumo de Distribuição")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Distribuído", f"${summary['total_distributed']:,.2f}")
        st.metric("Carteira BTC", f"${summary['total_to_wallet']:,.2f}")
    
    with col2:
        st.metric("Reinvestimento", f"${summary['total_reinvested']:,.2f}")
        st.metric("Operacional", f"${summary['total_operational']:,.2f}")
    
    with col3:
        st.metric("Taxas de Mineração", f"${summary['total_mining_fees']:,.2f}")
        st.metric("Pool de Liquidez", f"${summary['total_liquidity']:,.2f}")
    
    # Informações da carteira
    st.subheader("Carteira BTC de Destino")
    
    st.code(summary["btc_wallet"], language=None)
    
    # Gráfico de distribuição
    st.subheader("Alocação de Lucros")
    
    # Prepara dados para o gráfico
    allocation_data = {
        "categoria": ["Carteira BTC", "Reinvestimento", "Operacional", "Taxas de Mineração", "Pool de Liquidez"],
        "percentual": [
            distributor.distribution_rules["wallet_btc"],
            distributor.distribution_rules["reinvestment"],
            distributor.distribution_rules["operational"],
            distributor.distribution_rules["mining_fees"],
            distributor.distribution_rules["liquidity_pool"]
        ]
    }
    
    # Cria o gráfico de pizza
    fig = px.pie(
        names=allocation_data["categoria"],
        values=allocation_data["percentual"],
        title="Alocação de Lucros (%)",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detalhamento do reinvestimento
    st.subheader("Detalhamento do Reinvestimento (20% do total)")
    
    # Prepara dados para o gráfico
    reinvest_data = {
        "categoria": ["Yield Farming", "Staking", "Trading", "Airdrops"],
        "percentual": [
            distributor.reinvestment_allocation["yield_farming"],
            distributor.reinvestment_allocation["staking"],
            distributor.reinvestment_allocation["trading"],
            distributor.reinvestment_allocation["airdrops"]
        ]
    }
    
    # Cria o gráfico de pizza
    fig2 = px.pie(
        names=reinvest_data["categoria"],
        values=reinvest_data["percentual"],
        title="Alocação de Reinvestimento (%)",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Histórico de distribuições
    st.subheader("Histórico de Distribuições")
    
    # Selecionar o período
    period = st.selectbox("Período", ["7 dias", "30 dias", "90 dias"], index=0)
    
    days = int(period.split()[0])
    history = distributor.get_distribution_history(days=days)
    
    if history:
        # Prepara dados para o gráfico
        dates = [h["timestamp"] for h in history]
        profits = [h["profit"] for h in history]
        
        # Cria o gráfico de linha
        fig3 = go.Figure()
        
        fig3.add_trace(go.Scatter(
            x=dates,
            y=profits,
            mode='lines+markers',
            name='Lucro Distribuído',
            line=dict(color='green', width=2)
        ))
        
        fig3.update_layout(
            title=f'Lucro Distribuído nos Últimos {days} Dias',
            xaxis_title='Data',
            yaxis_title='Valor (USD)'
        )
        
        st.plotly_chart(fig3, use_container_width=True)
        
        # Tabela de distribuições
        st.subheader("Detalhes das Distribuições")
        
        # Prepara dados para a tabela
        table_data = []
        for h in history:
            table_data.append({
                "Data/Hora": h["timestamp"].strftime("%d/%m/%Y %H:%M"),
                "Lucro Total": f"${h['profit']:,.2f}",
                "Para Carteira": f"${h['distribution']['wallet_btc']:,.2f}",
                "Reinvestimento": f"${h['distribution']['reinvestment']:,.2f}",
                "Operacional": f"${h['distribution']['operational']:,.2f}",
                "Taxas de Mineração": f"${h['distribution']['mining_fees']:,.2f}",
                "Pool de Liquidez": f"${h['distribution']['liquidity_pool']:,.2f}"
            })
        
        # Exibe a tabela
        st.dataframe(pd.DataFrame(table_data), use_container_width=True)
    else:
        st.info(f"Nenhuma distribuição nos últimos {days} dias.")
    
    # Transações recentes
    st.subheader("Transações Recentes")
    
    recent_tx = distributor.get_recent_transactions(limit=20)
    
    if recent_tx:
        # Prepara dados para a tabela
        tx_data = []
        for tx in recent_tx:
            tx_data.append({
                "Data/Hora": tx["timestamp"].strftime("%d/%m/%Y %H:%M:%S"),
                "Tipo": tx["type"],
                "Valor": f"${tx['amount']:,.2f}",
                "Status": tx["status"],
                "Detalhes": tx.get("address", "") if "address" in tx else "",
            })
        
        # Exibe a tabela
        st.dataframe(pd.DataFrame(tx_data), use_container_width=True)
    else:
        st.info("Nenhuma transação recente.")
    
    # Distribuição manual (para testes)
    if st.session_state.show_advanced:
        st.subheader("Distribuição Manual (Teste)")
        
        test_profit = st.number_input("Lucro a Distribuir ($)", min_value=1.0, max_value=1000000.0, value=1000.0)
        
        if st.button("Realizar Distribuição Manual"):
            with st.spinner("Distribuindo lucro..."):
                distribution = distributor.manual_distribute(test_profit)
                
                # Mostra resultado
                st.success(f"Distribuição manual de ${test_profit:,.2f} realizada com sucesso!")
                
                # Detalhes da distribuição
                st.json({
                    "Carteira BTC": f"${distribution['wallet_btc']:,.2f}",
                    "Reinvestimento": f"${distribution['reinvestment']:,.2f}",
                    "Detalhes do Reinvestimento": {
                        k: f"${v:,.2f}" for k, v in distribution['reinvestment_detail'].items()
                    },
                    "Operacional": f"${distribution['operational']:,.2f}",
                    "Taxas de Mineração": f"${distribution['mining_fees']:,.2f}",
                    "Pool de Liquidez": f"${distribution['liquidity_pool']:,.2f}"
                })
                
                # Recarrega a página
                st.rerun()
    
    # Aviso legal
    st.warning("""
    **AVISO:** O sistema de distribuição automática de lucros está configurado para enviar 
    50% do lucro a cada hora para a carteira BTC designada. As demais alocações são 
    processadas automaticamente dentro da plataforma para maximizar o desempenho geral.
    """)