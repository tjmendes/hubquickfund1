import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random

class FlashLoanManager:
    """Gerencia operações de flash loan em diferentes protocolos DeFi"""
    
    def __init__(self):
        """Inicializa o gerenciador de flash loans"""
        self.enabled = True
        self.protocols = {
            "aave": {
                "name": "Aave",
                "fee": 0.09,  # 0.09% de taxa
                "max_loan": 10000000,  # $10M máximo
                "tokens": ["DAI", "USDC", "USDT", "ETH", "WBTC", "LINK", "UNI"],
                "liquidity": {
                    "DAI": 250000000,
                    "USDC": 500000000,
                    "USDT": 400000000,
                    "ETH": 150000000,
                    "WBTC": 80000000,
                    "LINK": 30000000,
                    "UNI": 15000000
                }
            },
            "dydx": {
                "name": "dYdX",
                "fee": 0.00,  # Sem taxa (cobra no spread)
                "max_loan": 5000000,  # $5M máximo
                "tokens": ["DAI", "USDC", "ETH", "WBTC"],
                "liquidity": {
                    "DAI": 120000000,
                    "USDC": 250000000,
                    "ETH": 100000000,
                    "WBTC": 50000000
                }
            },
            "compound": {
                "name": "Compound",
                "fee": 0.03,  # 0.03% de taxa (simulada, na realidade usa outro modelo)
                "max_loan": 8000000,  # $8M máximo
                "tokens": ["DAI", "USDC", "USDT", "ETH", "WBTC", "LINK"],
                "liquidity": {
                    "DAI": 180000000,
                    "USDC": 350000000,
                    "USDT": 280000000,
                    "ETH": 120000000,
                    "WBTC": 60000000,
                    "LINK": 20000000
                }
            },
            "maker": {
                "name": "MakerDAO",
                "fee": 0.05,  # 0.05% de taxa (simulada)
                "max_loan": 7000000,  # $7M máximo
                "tokens": ["DAI", "ETH", "WBTC"],
                "liquidity": {
                    "DAI": 500000000,
                    "ETH": 80000000,
                    "WBTC": 40000000
                }
            },
            "balancer": {
                "name": "Balancer",
                "fee": 0.08,  # 0.08% de taxa
                "max_loan": 3000000,  # $3M máximo
                "tokens": ["DAI", "USDC", "USDT", "ETH", "WBTC"],
                "liquidity": {
                    "DAI": 80000000,
                    "USDC": 120000000,
                    "USDT": 90000000,
                    "ETH": 60000000,
                    "WBTC": 30000000
                }
            }
        }
        
        self.executed_loans = []
        self.current_opportunities = self._init_opportunities()
        self.historic_performance = self._init_historic_performance()
        
    def _init_opportunities(self):
        """Inicializa oportunidades de flash loan para demonstração"""
        opportunities = []
        
        # Algumas oportunidades simuladas de arbitragem via flash loan
        opportunities.append({
            "id": "FL001",
            "type": "arbitragem",
            "description": "Arbitragem ETH entre Binance e Coinbase",
            "protocol": "aave",
            "token": "ETH",
            "loan_amount": 100,
            "loan_value_usd": 250000,
            "fee": 225,
            "expected_profit": 875,
            "expected_profit_pct": 0.35,
            "risk_level": "baixo",
            "execution_time_ms": 215,
            "timestamp": datetime.now() - timedelta(minutes=25)
        })
        
        opportunities.append({
            "id": "FL002",
            "type": "arbitragem",
            "description": "Arbitragem USDC/USDT entre Uniswap e Sushiswap",
            "protocol": "compound",
            "token": "USDC",
            "loan_amount": 500000,
            "loan_value_usd": 500000,
            "fee": 150,
            "expected_profit": 750,
            "expected_profit_pct": 0.15,
            "risk_level": "muito baixo",
            "execution_time_ms": 180,
            "timestamp": datetime.now() - timedelta(minutes=18)
        })
        
        opportunities.append({
            "id": "FL003",
            "type": "dex_arbitragem",
            "description": "Arbitragem WBTC via Curve e Balancer",
            "protocol": "aave",
            "token": "WBTC",
            "loan_amount": 5,
            "loan_value_usd": 150000,
            "fee": 135,
            "expected_profit": 620,
            "expected_profit_pct": 0.41,
            "risk_level": "médio",
            "execution_time_ms": 230,
            "timestamp": datetime.now() - timedelta(minutes=10)
        })
        
        opportunities.append({
            "id": "FL004",
            "type": "liquidacao",
            "description": "Liquidação de empréstimo Compound",
            "protocol": "dydx",
            "token": "DAI",
            "loan_amount": 350000,
            "loan_value_usd": 350000,
            "fee": 0,
            "expected_profit": 1750,
            "expected_profit_pct": 0.5,
            "risk_level": "médio-alto",
            "execution_time_ms": 275,
            "timestamp": datetime.now() - timedelta(minutes=5)
        })
        
        opportunities.append({
            "id": "FL005",
            "type": "arbitragem",
            "description": "Arbitragem LINK entre Binance e KuCoin",
            "protocol": "compound",
            "token": "LINK",
            "loan_amount": 15000,
            "loan_value_usd": 200000,
            "fee": 60,
            "expected_profit": 640,
            "expected_profit_pct": 0.32,
            "risk_level": "baixo",
            "execution_time_ms": 195,
            "timestamp": datetime.now() - timedelta(minutes=2)
        })
        
        return opportunities
    
    def _init_historic_performance(self):
        """Inicializa dados históricos de desempenho para demonstração"""
        # Dados dos últimos 30 dias
        end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = end_date - timedelta(days=30)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Dados base
        base_loans = 50
        base_volume = 1000000
        base_profit = 5000
        base_success = 95
        
        # Listas para armazenar os dados
        loan_counts = []
        volumes = []
        profits = []
        success_rates = []
        
        # Gera dados com tendência de crescimento
        for i in range(len(dates)):
            progress = i / (len(dates) - 1)  # 0 a 1
            noise = np.random.normal(0, 0.1)  # Adiciona alguma variação
            growth = 1 + progress * 0.5 + noise  # Fator de crescimento
            
            loan_counts.append(int(base_loans * growth))
            volumes.append(int(base_volume * growth))
            profits.append(int(base_profit * growth))
            success_rates.append(min(100, base_success + progress * 5))
        
        # Cria DataFrame
        df = pd.DataFrame({
            'date': dates,
            'loans_executed': loan_counts,
            'volume_usd': volumes,
            'profit_usd': profits,
            'success_rate': success_rates
        })
        
        return df
    
    def get_available_protocols(self):
        """Retorna os protocolos disponíveis para flash loans"""
        return self.protocols
    
    def get_token_liquidity(self, protocol, token):
        """Retorna a liquidez disponível para um token em um protocolo"""
        if protocol in self.protocols and token in self.protocols[protocol]["tokens"]:
            return self.protocols[protocol]["liquidity"].get(token, 0)
        return 0
    
    def calculate_fee(self, protocol, token, amount):
        """Calcula a taxa para um flash loan"""
        if protocol in self.protocols:
            fee_pct = self.protocols[protocol]["fee"]
            return amount * fee_pct / 100
        return 0
    
    def simulate_flash_loan(self, protocol, token, amount):
        """Simula um flash loan sem executar a transação"""
        result = {
            "success": False,
            "message": "",
            "details": {}
        }
        
        # Verifica se o protocolo existe
        if protocol not in self.protocols:
            result["message"] = f"Protocolo {protocol} não suportado"
            return result
        
        # Verifica se o token é suportado pelo protocolo
        if token not in self.protocols[protocol]["tokens"]:
            result["message"] = f"Token {token} não suportado pelo protocolo {self.protocols[protocol]['name']}"
            return result
        
        # Verifica se há liquidez suficiente
        liquidity = self.get_token_liquidity(protocol, token)
        if amount > liquidity:
            result["message"] = f"Liquidez insuficiente. Disponível: {liquidity:,.2f} {token}"
            return result
        
        # Verifica limite máximo do protocolo
        protocol_info = self.protocols[protocol]
        token_price = self._get_token_price(token)
        amount_usd = amount * token_price
        
        if amount_usd > protocol_info["max_loan"]:
            result["message"] = f"Valor excede o limite máximo do protocolo ({protocol_info['max_loan']:,.2f} USD)"
            return result
        
        # Calcula taxa
        fee_pct = protocol_info["fee"]
        fee = amount * fee_pct / 100
        fee_usd = fee * token_price
        
        # Simulação bem-sucedida
        result["success"] = True
        result["message"] = "Simulação bem-sucedida"
        result["details"] = {
            "protocol": protocol,
            "protocol_name": protocol_info["name"],
            "token": token,
            "amount": amount,
            "amount_usd": amount_usd,
            "fee_pct": fee_pct,
            "fee": fee,
            "fee_usd": fee_usd,
            "liquidity": liquidity,
            "max_loan": protocol_info["max_loan"],
            "execution_time_estimate_ms": self._estimate_execution_time(protocol, amount_usd)
        }
        
        return result
    
    def execute_flash_loan(self, protocol, token, amount, opportunity_id=None):
        """Executa um flash loan simulado"""
        # Primeiro simula para verificar viabilidade
        simulation = self.simulate_flash_loan(protocol, token, amount)
        
        if not simulation["success"]:
            return simulation
        
        # Simula a execução
        result = {
            "success": True,
            "transaction_hash": f"0x{random.randint(0, 10**50):x}",
            "execution_time_ms": self._estimate_execution_time(protocol, simulation["details"]["amount_usd"]),
            "timestamp": datetime.now(),
            **simulation["details"]
        }
        
        # Adiciona ao histórico
        self.executed_loans.append({
            "id": f"TX{len(self.executed_loans) + 1:04d}",
            "protocol": protocol,
            "token": token,
            "amount": amount,
            "amount_usd": simulation["details"]["amount_usd"],
            "fee": simulation["details"]["fee"],
            "fee_usd": simulation["details"]["fee_usd"],
            "profit": 0,  # Será atualizado quando a estratégia for executada
            "transaction_hash": result["transaction_hash"],
            "execution_time_ms": result["execution_time_ms"],
            "timestamp": result["timestamp"],
            "opportunity_id": opportunity_id
        })
        
        return result
    
    def get_opportunities(self):
        """Retorna as oportunidades atuais de flash loan"""
        return self.current_opportunities
    
    def get_executed_loans(self):
        """Retorna o histórico de flash loans executados"""
        return self.executed_loans
    
    def get_historic_performance(self):
        """Retorna os dados históricos de desempenho"""
        return self.historic_performance
    
    def _get_token_price(self, token):
        """Retorna o preço atual de um token (simulado)"""
        prices = {
            "DAI": 1.0,
            "USDC": 1.0,
            "USDT": 1.0,
            "ETH": 2500.0,
            "WBTC": 30000.0,
            "LINK": 13.5,
            "UNI": 8.2
        }
        return prices.get(token, 1.0)
    
    def _estimate_execution_time(self, protocol, amount_usd):
        """Estima o tempo de execução de um flash loan com base no protocolo e valor"""
        # Valores base para cada protocolo (em milissegundos)
        base_times = {
            "aave": 200,
            "dydx": 180,
            "compound": 220,
            "maker": 250,
            "balancer": 210
        }
        
        # Fator de escala com base no valor (valores maiores levam um pouco mais de tempo)
        scale_factor = 1.0 + (amount_usd / 1000000) * 0.1  # +10% para cada $1M
        
        # Limite o fator de escala
        scale_factor = min(1.5, scale_factor)
        
        # Adiciona variação aleatória
        random_factor = random.uniform(0.9, 1.1)
        
        return int(base_times.get(protocol, 200) * scale_factor * random_factor)
    
    def generate_new_opportunities(self):
        """Gera novas oportunidades de flash loan (simulado)"""
        # Tipos de oportunidades
        opportunity_types = ["arbitragem", "dex_arbitragem", "liquidacao"]
        
        # Protocolos disponíveis
        protocol_list = list(self.protocols.keys())
        
        # Número de novas oportunidades
        num_new = random.randint(1, 3)
        
        new_opportunities = []
        
        for i in range(num_new):
            # Seleção aleatória de parâmetros
            opp_type = random.choice(opportunity_types)
            protocol = random.choice(protocol_list)
            protocol_info = self.protocols[protocol]
            token = random.choice(protocol_info["tokens"])
            token_price = self._get_token_price(token)
            
            # Valores com base no tipo
            if opp_type == "arbitragem":
                loan_value_usd = random.uniform(50000, 500000)
                loan_amount = loan_value_usd / token_price
                profit_pct = random.uniform(0.1, 0.4)
            elif opp_type == "dex_arbitragem":
                loan_value_usd = random.uniform(100000, 1000000)
                loan_amount = loan_value_usd / token_price
                profit_pct = random.uniform(0.2, 0.5)
            else:  # liquidacao
                loan_value_usd = random.uniform(200000, 1500000)
                loan_amount = loan_value_usd / token_price
                profit_pct = random.uniform(0.3, 0.7)
            
            # Cálculos baseados nos valores
            fee = loan_value_usd * protocol_info["fee"] / 100
            expected_profit = loan_value_usd * profit_pct / 100
            
            # Determina nível de risco
            if profit_pct < 0.2:
                risk_level = "muito baixo"
            elif profit_pct < 0.3:
                risk_level = "baixo"
            elif profit_pct < 0.5:
                risk_level = "médio"
            else:
                risk_level = "médio-alto"
            
            # Descrições baseadas no tipo
            description = ""
            if opp_type == "arbitragem":
                exchanges = random.sample(["Binance", "Coinbase", "Kraken", "KuCoin", "Bybit"], 2)
                description = f"Arbitragem {token} entre {exchanges[0]} e {exchanges[1]}"
            elif opp_type == "dex_arbitragem":
                dexes = random.sample(["Uniswap", "Sushiswap", "Curve", "Balancer", "PancakeSwap"], 2)
                description = f"Arbitragem {token} via {dexes[0]} e {dexes[1]}"
            else:  # liquidacao
                lending_platforms = ["Compound", "Aave", "MakerDAO", "Venus"]
                platform = random.choice(lending_platforms)
                description = f"Liquidação de empréstimo {platform}"
            
            # Cria a oportunidade
            new_opp = {
                "id": f"FL{len(self.current_opportunities) + i + 1:03d}",
                "type": opp_type,
                "description": description,
                "protocol": protocol,
                "token": token,
                "loan_amount": round(loan_amount, 6),
                "loan_value_usd": round(loan_value_usd, 2),
                "fee": round(fee, 2),
                "expected_profit": round(expected_profit, 2),
                "expected_profit_pct": round(profit_pct, 2),
                "risk_level": risk_level,
                "execution_time_ms": self._estimate_execution_time(protocol, loan_value_usd),
                "timestamp": datetime.now() - timedelta(minutes=random.randint(0, 5))
            }
            
            new_opportunities.append(new_opp)
        
        # Adiciona as novas oportunidades à lista existente
        self.current_opportunities.extend(new_opportunities)
        
        # Limita a 10 oportunidades
        if len(self.current_opportunities) > 10:
            self.current_opportunities = self.current_opportunities[-10:]
        
        return new_opportunities

# Singleton para uso em toda a aplicação
_flash_loan_manager = None

def get_flash_loan_manager():
    """Retorna uma instância do gerenciador de flash loans"""
    global _flash_loan_manager
    if _flash_loan_manager is None:
        _flash_loan_manager = FlashLoanManager()
    return _flash_loan_manager

def render_page():
    st.header("Flash Loans Estratégicos")
    
    st.markdown("""
    ### Sistema avançado de arbitragem sem capital inicial
    
    Flash Loans permitem pegar empréstimos instantâneos sem colateral, desde que sejam devolvidos
    na mesma transação. Esta funcionalidade revolucionária possibilita executar operações de arbitragem, 
    liquidações e estratégias complexas sem necessidade de capital inicial.
    """)
    
    # Obtém instância do gerenciador
    manager = get_flash_loan_manager()
    
    # Tabs para organizar o conteúdo
    tab1, tab2, tab3, tab4 = st.tabs([
        "Oportunidades", "Simulador", "Histórico", "Performance"
    ])
    
    with tab1:
        st.subheader("Oportunidades de Flash Loan")
        
        # Botão para atualizar oportunidades
        if st.button("Buscar Novas Oportunidades", key="refresh_opportunities"):
            with st.spinner("Analisando mercado para oportunidades de flash loan..."):
                new_opps = manager.generate_new_opportunities()
                st.success(f"Encontradas {len(new_opps)} novas oportunidades de flash loan!")
        
        # Obtém oportunidades atuais
        opportunities = manager.get_opportunities()
        
        if not opportunities:
            st.info("Nenhuma oportunidade de flash loan disponível no momento. Clique em 'Buscar Novas Oportunidades'.")
        else:
            # Cria DataFrame para exibição
            opps_df = pd.DataFrame(opportunities)
            
            # Formata colunas para exibição
            display_df = opps_df.copy()
            display_df["token_amount"] = display_df["loan_amount"].apply(lambda x: f"{x:,.6g}")
            display_df["valor_usd"] = display_df["loan_value_usd"].apply(lambda x: f"${x:,.2f}")
            display_df["taxa"] = display_df["fee"].apply(lambda x: f"${x:,.2f}")
            display_df["lucro_esperado"] = display_df["expected_profit"].apply(lambda x: f"${x:,.2f}")
            display_df["lucro_pct"] = display_df["expected_profit_pct"].apply(lambda x: f"{x:.2f}%")
            display_df["tempo_execucao"] = display_df["execution_time_ms"].apply(lambda x: f"{x} ms")
            display_df["data_hora"] = display_df["timestamp"].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
            
            # Seleciona e renomeia colunas para exibição
            display_df = display_df[[
                "id", "description", "protocol", "token", "token_amount", "valor_usd", 
                "taxa", "lucro_esperado", "lucro_pct", "risk_level", "tempo_execucao", "data_hora"
            ]]
            
            display_df.columns = [
                "ID", "Descrição", "Protocolo", "Token", "Quantidade", "Valor (USD)", 
                "Taxa", "Lucro Esperado", "% Lucro", "Risco", "Tempo Exec.", "Data/Hora"
            ]
            
            # Exibe tabela de oportunidades
            st.dataframe(display_df, use_container_width=True)
            
            # Permite executar uma oportunidade selecionada
            st.subheader("Executar Oportunidade")
            
            selected_opp = st.selectbox(
                "Selecione uma oportunidade para executar",
                options=[f"{o['id']} - {o['description']} ({o['token']} {o['loan_amount']:,.6g})" for o in opportunities],
                index=0
            )
            
            selected_id = selected_opp.split(" - ")[0]
            opp = next((o for o in opportunities if o["id"] == selected_id), None)
            
            if opp:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Protocolo:** {opp['protocol'].upper()}")
                    st.markdown(f"**Token:** {opp['token']}")
                
                with col2:
                    st.markdown(f"**Quantidade:** {opp['loan_amount']:,.6g}")
                    st.markdown(f"**Valor USD:** ${opp['loan_value_usd']:,.2f}")
                
                with col3:
                    st.markdown(f"**Taxa:** ${opp['fee']:,.2f}")
                    st.markdown(f"**Lucro Esperado:** ${opp['expected_profit']:,.2f} ({opp['expected_profit_pct']:.2f}%)")
                
                if st.button("Executar Flash Loan", type="primary"):
                    with st.spinner(f"Executando flash loan para {opp['description']}..."):
                        # Simula tempo de execução
                        time.sleep(2)
                        
                        result = manager.execute_flash_loan(
                            opp["protocol"], 
                            opp["token"], 
                            opp["loan_amount"], 
                            opp["id"]
                        )
                        
                        if result["success"]:
                            st.success(f"Flash loan executado com sucesso! Transação: {result['transaction_hash'][:10]}...")
                            
                            # Remove a oportunidade executada
                            manager.current_opportunities = [o for o in manager.current_opportunities if o["id"] != opp["id"]]
                            
                            # Rerun para atualizar a interface
                            st.rerun()
                        else:
                            st.error(f"Falha ao executar flash loan: {result['message']}")
    
    with tab2:
        st.subheader("Simulador de Flash Loan")
        
        st.markdown("""
        Use este simulador para planejar operações de flash loan e verificar viabilidade,
        taxas e requisitos.
        """)
        
        # Obtém protocolos disponíveis
        protocols = manager.get_available_protocols()
        
        # Formulário para simulação
        col1, col2 = st.columns(2)
        
        with col1:
            # Seleção de protocolo
            selected_protocol = st.selectbox(
                "Protocolo",
                options=list(protocols.keys()),
                format_func=lambda x: protocols[x]["name"]
            )
            
            # Informações do protocolo selecionado
            protocol_info = protocols[selected_protocol]
            
            st.markdown(f"""
            **Taxa:** {protocol_info['fee']}%  
            **Empréstimo Máximo:** ${protocol_info['max_loan']:,.2f}
            """)
            
            # Seleção de token
            selected_token = st.selectbox(
                "Token",
                options=protocol_info["tokens"]
            )
            
            # Informações de liquidez
            token_liquidity = manager.get_token_liquidity(selected_protocol, selected_token)
            st.markdown(f"**Liquidez Disponível:** {token_liquidity:,.2f} {selected_token}")
            
            # Determina preço do token para conversão
            token_price = manager._get_token_price(selected_token)
        
        with col2:
            # Entrada de valor
            loan_amount = st.number_input(
                f"Quantidade ({selected_token})",
                min_value=0.000001,
                max_value=float(token_liquidity),
                value=min(1.0, token_liquidity / 10),
                format="%.6f"
            )
            
            # Valor em USD
            loan_value_usd = loan_amount * token_price
            st.markdown(f"**Valor em USD:** ${loan_value_usd:,.2f}")
            
            # Calcula taxa
            fee = manager.calculate_fee(selected_protocol, selected_token, loan_amount)
            fee_usd = fee * token_price
            st.markdown(f"**Taxa:** {fee:,.6f} {selected_token} (${fee_usd:,.2f})")
            
            # Botão para simulação
            simulate_button = st.button("Simular Flash Loan")
        
        # Executa simulação
        if simulate_button:
            with st.spinner("Simulando flash loan..."):
                result = manager.simulate_flash_loan(selected_protocol, selected_token, loan_amount)
                
                if result["success"]:
                    st.success("Simulação bem-sucedida!")
                    
                    details = result["details"]
                    
                    # Exibe resultados detalhados
                    st.subheader("Resultados da Simulação")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        **Protocolo:** {details['protocol_name']}  
                        **Token:** {details['token']}  
                        **Quantidade:** {details['amount']:,.6f}  
                        **Valor USD:** ${details['amount_usd']:,.2f}
                        """)
                    
                    with col2:
                        st.markdown(f"""
                        **Taxa:** {details['fee']:,.6f} {details['token']} (${details['fee_usd']:,.2f})  
                        **Taxa (%):** {details['fee_pct']}%  
                        **Tempo Est. Execução:** {details['execution_time_estimate_ms']} ms
                        """)
                    
                    # Campos para estratégia
                    st.subheader("Defina sua Estratégia")
                    
                    strategy_type = st.selectbox(
                        "Tipo de Estratégia",
                        options=["Arbitragem", "Liquidação", "DEX Swap", "Rebalanceamento"],
                        index=0
                    )
                    
                    expected_profit = st.number_input(
                        "Lucro Esperado (USD)",
                        min_value=0.0,
                        value=details['fee_usd'] * 2  # Valor padrão: 2x a taxa
                    )
                    
                    profit_pct = (expected_profit / details['amount_usd']) * 100
                    
                    st.markdown(f"""
                    **Lucro Líquido Esperado:** ${expected_profit - details['fee_usd']:,.2f}  
                    **Retorno sobre Valor (%):** {profit_pct:.2f}%
                    """)
                    
                    # Botão para execução
                    if st.button("Executar Estratégia", type="primary"):
                        with st.spinner("Executando flash loan..."):
                            # Simula execução com delay
                            time.sleep(2)
                            
                            result = manager.execute_flash_loan(
                                selected_protocol, 
                                selected_token, 
                                loan_amount
                            )
                            
                            if result["success"]:
                                st.success(f"Flash loan executado com sucesso! Transação: {result['transaction_hash'][:10]}...")
                                
                                # Adiciona lucro ao registro (simulação)
                                executed_loan = manager.executed_loans[-1]
                                executed_loan["profit"] = expected_profit
                                executed_loan["strategy"] = strategy_type
                                
                                # Rerun para atualizar a interface
                                st.rerun()
                            else:
                                st.error(f"Falha ao executar flash loan: {result['message']}")
                
                else:
                    st.error(f"Simulação falhou: {result['message']}")
    
    with tab3:
        st.subheader("Histórico de Flash Loans")
        
        # Obtém histórico de empréstimos
        executed_loans = manager.get_executed_loans()
        
        if not executed_loans:
            st.info("Nenhum flash loan foi executado até o momento.")
        else:
            # Cria DataFrame para exibição
            loans_df = pd.DataFrame(executed_loans)
            
            # Formata colunas para exibição
            display_df = loans_df.copy()
            display_df["token_amount"] = display_df["amount"].apply(lambda x: f"{x:,.6g}")
            display_df["valor_usd"] = display_df["amount_usd"].apply(lambda x: f"${x:,.2f}")
            display_df["taxa_usd"] = display_df["fee_usd"].apply(lambda x: f"${x:,.2f}")
            display_df["lucro"] = display_df["profit"].apply(lambda x: f"${x:,.2f}" if x > 0 else "-")
            display_df["data_hora"] = display_df["timestamp"].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
            display_df["tx_hash"] = display_df["transaction_hash"].apply(lambda x: f"{x[:10]}...")
            
            # Seleciona e renomeia colunas para exibição
            display_df = display_df[[
                "id", "protocol", "token", "token_amount", "valor_usd", 
                "taxa_usd", "lucro", "tx_hash", "data_hora"
            ]]
            
            display_df.columns = [
                "ID", "Protocolo", "Token", "Quantidade", "Valor (USD)", 
                "Taxa (USD)", "Lucro", "Tx Hash", "Data/Hora"
            ]
            
            # Exibe tabela de empréstimos
            st.dataframe(display_df, use_container_width=True)
            
            # Gráfico de volume de flash loans
            st.subheader("Volume de Flash Loans por Protocolo")
            
            # Agrupa por protocolo
            protocol_volume = loans_df.groupby("protocol")["amount_usd"].sum().reset_index()
            protocol_volume.columns = ["Protocolo", "Volume (USD)"]
            
            # Formata nomes dos protocolos
            protocol_volume["Protocolo"] = protocol_volume["Protocolo"].apply(
                lambda x: protocols.get(x, {}).get("name", x.upper())
            )
            
            fig = px.pie(
                protocol_volume,
                values="Volume (USD)",
                names="Protocolo",
                title="Distribuição de Volume por Protocolo",
                hole=0.4
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Performance e Estatísticas")
        
        # Obtém dados históricos de performance
        historic_df = manager.get_historic_performance()
        
        # Métricas resumidas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_loans = historic_df["loans_executed"].sum()
            st.metric("Total de Operações", format(int(total_loans), ","))
        
        with col2:
            total_volume = historic_df["volume_usd"].sum()
            st.metric("Volume Total", f"${total_volume:,.2f}")
        
        with col3:
            total_profit = historic_df["profit_usd"].sum()
            st.metric("Lucro Total", f"${total_profit:,.2f}")
        
        with col4:
            avg_success = historic_df["success_rate"].mean()
            st.metric("Taxa Média de Sucesso", f"{avg_success:.2f}%")
        
        # Gráficos de tendência
        st.subheader("Tendências de Performance")
        
        # Tabs para diferentes gráficos
        tab_a, tab_b, tab_c, tab_d = st.tabs([
            "Operações", "Volume", "Lucro", "Taxa de Sucesso"
        ])
        
        with tab_a:
            fig = px.line(
                historic_df,
                x="date",
                y="loans_executed",
                markers=True,
                title="Número de Operações por Dia"
            )
            fig.update_layout(
                xaxis_title="Data",
                yaxis_title="Operações"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab_b:
            fig = px.line(
                historic_df,
                x="date",
                y="volume_usd",
                markers=True,
                title="Volume de Flash Loans por Dia (USD)"
            )
            fig.update_layout(
                xaxis_title="Data",
                yaxis_title="Volume (USD)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab_c:
            fig = px.line(
                historic_df,
                x="date",
                y="profit_usd",
                markers=True,
                title="Lucro Diário (USD)"
            )
            fig.update_layout(
                xaxis_title="Data",
                yaxis_title="Lucro (USD)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab_d:
            fig = px.line(
                historic_df,
                x="date",
                y="success_rate",
                markers=True,
                title="Taxa de Sucesso Diária (%)"
            )
            fig.update_layout(
                xaxis_title="Data",
                yaxis_title="Taxa de Sucesso (%)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Informações educacionais
        st.subheader("Como Funcionam Flash Loans")
        
        st.markdown("""
        ### O Conceito de Flash Loans
        
        Flash Loans são empréstimos instantâneos que devem ser tomados e pagos na mesma transação blockchain.
        Não é necessário fornecer garantias, pois tudo acontece atomicamente - ou a transação completa
        é bem-sucedida, ou falha por completo.
        
        ### Casos de Uso Comuns:
        
        1. **Arbitragem** - Aproveitar diferenças de preço entre exchanges
        2. **Liquidações** - Participar de liquidações em protocolos DeFi
        3. **Rebalanceamento de Dívida** - Refinanciar posições entre protocolos
        4. **Self-Liquidation** - Liquidar suas próprias posições para economizar em taxas
        5. **Swap Collateral** - Trocar colaterais sem precisar fechar posições
        
        ### Protocolos Populares:
        
        - **Aave** - Um dos primeiros a implementar flash loans
        - **dYdX** - Oferece flash loans sem taxa explícita
        - **Compound** - Implementa flash loans através de seu protocolo de liquidez
        - **MakerDAO** - Permite operações flash através do mecanismo DSProxy
        - **Balancer** - Permite flash swaps semelhantes ao Uniswap
        """)
        
        # Aviso legal
        st.warning("""
        **AVISO:** Esta ferramenta está em modo de demonstração. Os dados mostrados são simulados 
        para fins de visualização. Em um ambiente de produção, seriam necessárias carteiras com 
        criptomoedas reais e conexão com smart contracts.
        """)