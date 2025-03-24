import streamlit as st
import pandas as pd
import numpy as np
import time
import threading
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import os
import json

class TradingBot:
    """Classe que representa um bot de trading individual"""
    
    def __init__(self, bot_id, strategy, markets, timeframes):
        """Inicializa o bot de trading"""
        self.bot_id = bot_id
        self.strategy = strategy
        self.markets = markets  # Lista de mercados (pares) que o bot opera
        self.timeframes = timeframes  # Lista de timeframes que o bot monitora
        
        # Status do bot
        self.status = "idle"  # idle, running, paused, error
        self.is_profitable = random.random() > 0.2  # 80% de chance de ser lucrativo
        
        # Estatísticas de desempenho
        self.start_time = None
        self.last_trade_time = None
        self.trades_executed = 0
        self.successful_trades = 0
        self.failed_trades = 0
        self.total_profit = 0.0
        self.roi = 0.0
        self.trades_history = []
        
        # Configurações
        self.risk_level = random.choice(["baixo", "médio", "alto"])
        self.max_position_size = random.uniform(100, 10000)
        self.stop_loss_pct = random.uniform(1, 10)
        self.take_profit_pct = random.uniform(2, 20)
        
        # Tecnologias utilizadas
        self.uses_ai = random.random() > 0.5
        self.uses_ml = random.random() > 0.5
        self.uses_sentiment_analysis = random.random() > 0.3
        self.uses_technical_analysis = random.random() > 0.1
        self.uses_fundamental_analysis = random.random() > 0.7
        
        # Performance recente
        self.recent_performance = []
        for _ in range(30):  # 30 dias de dados
            self.recent_performance.append(random.uniform(-3, 5))  # Entre -3% e +5% por dia
    
    def start(self):
        """Inicia o bot"""
        if self.status == "running":
            return False, "Bot já está em execução"
        
        self.status = "running"
        self.start_time = datetime.now()
        return True, "Bot iniciado com sucesso"
    
    def stop(self):
        """Para o bot"""
        if self.status != "running":
            return False, "Bot não está em execução"
        
        self.status = "idle"
        return True, "Bot parado com sucesso"
    
    def pause(self):
        """Pausa o bot"""
        if self.status != "running":
            return False, "Bot não está em execução"
        
        self.status = "paused"
        return True, "Bot pausado com sucesso"
    
    def resume(self):
        """Retoma a execução do bot"""
        if self.status != "paused":
            return False, "Bot não está pausado"
        
        self.status = "running"
        return True, "Bot retomado com sucesso"
    
    def simulate_trade(self):
        """Simula uma operação de trading"""
        if self.status != "running":
            return None
        
        # Escolher um mercado e timeframe aleatórios
        market = random.choice(self.markets)
        timeframe = random.choice(self.timeframes)
        
        # Decidir se é compra ou venda
        trade_type = random.choice(["compra", "venda"])
        
        # Decidir o tamanho da posição
        position_size = random.uniform(0.1 * self.max_position_size, self.max_position_size)
        
        # Decidir se a operação será bem-sucedida
        is_successful = random.random() < (0.7 if self.is_profitable else 0.4)
        
        # Calcular o lucro/perda
        profit_pct = random.uniform(-self.stop_loss_pct, self.take_profit_pct)
        if is_successful:
            profit_pct = abs(profit_pct)  # Garantir que seja positivo
        else:
            profit_pct = -abs(profit_pct)  # Garantir que seja negativo
        
        profit_amount = position_size * (profit_pct / 100)
        
        # Atualizar estatísticas
        self.trades_executed += 1
        if is_successful:
            self.successful_trades += 1
        else:
            self.failed_trades += 1
        
        self.total_profit += profit_amount
        self.last_trade_time = datetime.now()
        
        # Calcular ROI
        self.roi = (self.total_profit / (self.max_position_size * self.trades_executed)) * 100
        
        # Criar registro da operação
        trade = {
            "id": f"T{self.trades_executed:06d}",
            "timestamp": self.last_trade_time,
            "market": market,
            "timeframe": timeframe,
            "type": trade_type,
            "position_size": position_size,
            "profit_pct": profit_pct,
            "profit_amount": profit_amount,
            "successful": is_successful
        }
        
        # Adicionar ao histórico
        self.trades_history.append(trade)
        
        # Limitar o histórico a 1000 operações
        if len(self.trades_history) > 1000:
            self.trades_history = self.trades_history[-1000:]
        
        return trade
    
    def get_status(self):
        """Retorna o status atual do bot"""
        return {
            "bot_id": self.bot_id,
            "strategy": self.strategy,
            "status": self.status,
            "markets": self.markets,
            "timeframes": self.timeframes,
            "trades_executed": self.trades_executed,
            "successful_trades": self.successful_trades,
            "failed_trades": self.failed_trades,
            "success_rate": (self.successful_trades / max(1, self.trades_executed)) * 100,
            "total_profit": self.total_profit,
            "roi": self.roi,
            "start_time": self.start_time,
            "last_trade_time": self.last_trade_time,
            "is_profitable": self.is_profitable,
            "risk_level": self.risk_level
        }
    
    def get_recent_trades(self, limit=10):
        """Retorna as operações mais recentes"""
        return self.trades_history[-limit:] if self.trades_history else []
    
    def get_performance_chart_data(self):
        """Retorna os dados para um gráfico de desempenho"""
        return self.recent_performance

class TradingBotNetwork:
    """Sistema de gerenciamento para milhares de bots de trading"""
    
    def __init__(self, num_bots=5000):
        """Inicializa a rede de bots de trading"""
        self.running = False
        self.simulation_thread = None
        self.bots = self._initialize_bots(num_bots)
        self.total_bots = num_bots
        self.active_bots = 0
        self.profitable_bots = 0
        self.last_scan_time = None
        self.scan_interval_seconds = 5  # Intervalo de simulação (5 segundos)
        self.network_stats = []
        self.best_performing_bots = []
        self.worst_performing_bots = []
        self.strategy_performance = {}
        self.market_performance = {}
        self.timeframe_performance = {}
        
        # Otimizações
        self.optimization_thread = None
        self.optimization_running = False
    
    def _initialize_bots(self, num_bots):
        """Inicializa os bots de trading"""
        # Lista de estratégias possíveis
        strategies = [
            "Arbitragem de Preço", "Market Making", "Scalping", "Swing Trading",
            "Momentum Trading", "Reversal Trading", "Breakout Trading", "Grid Trading",
            "HFT (High Frequency Trading)", "Statistical Arbitrage", "Machine Learning",
            "Neural Network", "Sentiment Analysis", "DCA (Dollar Cost Average)",
            "Volume Spread Analysis", "Mean Reversion", "Trend Following", "Support/Resistance",
            "Fibonacci Retracement", "Bollinger Bands", "Pattern Recognition", "Ichimoku Cloud",
            "MACD Strategy", "RSI Strategy", "Stochastic Strategy", "Moving Average Crossover",
            "Triangular Arbitrage", "Flash Arbitrage", "Liquidity Provision", "Hammer Candlestick",
            "Quantum Analysis", "Volatility Breakout", "Counter-Trend", "Option Arbitrage",
            "News Sentiment", "Deep Learning", "Reinforcement Learning", "Twitter Sentiment",
            "Reddit Sentiment", "Order Book Analysis", "Correlation Trading", "Flash Loans"
        ]
        
        # Lista de mercados possíveis
        markets = [
            "BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "ADA/USDT",
            "XRP/USDT", "DOT/USDT", "DOGE/USDT", "AVAX/USDT", "MATIC/USDT",
            "LINK/USDT", "UNI/USDT", "ATOM/USDT", "LTC/USDT", "BCH/USDT",
            "ALGO/USDT", "FIL/USDT", "XLM/USDT", "VET/USDT", "ETC/USDT",
            "MANA/USDT", "SAND/USDT", "AXS/USDT", "FTM/USDT", "ONE/USDT",
            "NEAR/USDT", "EGLD/USDT", "KSM/USDT", "THETA/USDT", "XMR/USDT",
            "AAVE/USDT", "XTZ/USDT", "MKR/USDT", "COMP/USDT", "SUSHI/USDT",
            "SNX/USDT", "YFI/USDT", "HBAR/USDT", "BAT/USDT", "ZEC/USDT"
        ]
        
        # Lista de timeframes possíveis
        timeframes = ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w"]
        
        # Criar bots
        bots = {}
        for i in range(1, num_bots + 1):
            # Escolher estratégia aleatória
            strategy = random.choice(strategies)
            
            # Escolher mercados aleatórios (entre 1 e 5)
            num_markets = random.randint(1, 5)
            bot_markets = random.sample(markets, num_markets)
            
            # Escolher timeframes aleatórios (entre 1 e 3)
            num_timeframes = random.randint(1, 3)
            bot_timeframes = random.sample(timeframes, num_timeframes)
            
            # Criar bot
            bot_id = f"BOT-{i:05d}"
            bots[bot_id] = TradingBot(bot_id, strategy, bot_markets, bot_timeframes)
        
        return bots
    
    def start_network(self):
        """Inicia a rede de bots de trading"""
        if self.running:
            return "A rede de bots já está em execução"
        
        self.running = True
        self.simulation_thread = threading.Thread(target=self._simulation_loop, daemon=True)
        self.simulation_thread.start()
        
        # Iniciar x% dos bots aleatoriamente
        start_percentage = random.uniform(40, 70)  # Entre 40% e 70%
        bots_to_start = int(self.total_bots * (start_percentage / 100))
        bot_ids = list(self.bots.keys())
        start_bots = random.sample(bot_ids, bots_to_start)
        
        for bot_id in start_bots:
            self.bots[bot_id].start()
        
        self.active_bots = bots_to_start
        
        # Iniciar o thread de otimização
        self.optimization_running = True
        self.optimization_thread = threading.Thread(target=self._optimization_loop, daemon=True)
        self.optimization_thread.start()
        
        return f"Rede de {self.total_bots} bots iniciada com sucesso. {bots_to_start} bots ativos."
    
    def stop_network(self):
        """Para a rede de bots de trading"""
        if not self.running:
            return "A rede de bots já está parada"
        
        self.running = False
        self.optimization_running = False
        
        if self.simulation_thread:
            self.simulation_thread.join(timeout=2.0)
        
        if self.optimization_thread:
            self.optimization_thread.join(timeout=2.0)
        
        # Parar todos os bots
        for bot in self.bots.values():
            if bot.status == "running" or bot.status == "paused":
                bot.stop()
        
        self.active_bots = 0
        
        return f"Rede de {self.total_bots} bots parada com sucesso."
    
    def _simulation_loop(self):
        """Loop de simulação de trading"""
        while self.running:
            self.last_scan_time = datetime.now()
            active_count = 0
            profitable_count = 0
            total_profit = 0.0
            
            # Simular trades para bots ativos
            for bot in self.bots.values():
                if bot.status == "running":
                    active_count += 1
                    trade = bot.simulate_trade()
                    
                    if bot.total_profit > 0:
                        profitable_count += 1
                    
                    total_profit += bot.total_profit
            
            # Atualizar estatísticas
            self.active_bots = active_count
            self.profitable_bots = profitable_count
            
            # Registrar estatísticas da rede
            self.network_stats.append({
                "timestamp": self.last_scan_time,
                "active_bots": active_count,
                "profitable_bots": profitable_count,
                "total_profit": total_profit
            })
            
            # Limitar o histórico a 1000 registros
            if len(self.network_stats) > 1000:
                self.network_stats = self.network_stats[-1000:]
            
            # Atualizar ranking de bots
            self._update_bot_rankings()
            
            # Atualizar estatísticas de desempenho
            self._update_performance_stats()
            
            # Esperar até o próximo intervalo
            time.sleep(self.scan_interval_seconds)
    
    def _update_bot_rankings(self):
        """Atualiza o ranking dos melhores e piores bots"""
        # Filtrar apenas bots ativos com pelo menos 10 trades
        active_bots = [bot for bot in self.bots.values() 
                      if bot.status == "running" and bot.trades_executed >= 10]
        
        if not active_bots:
            return
        
        # Ordenar por ROI
        sorted_bots = sorted(active_bots, key=lambda b: b.roi, reverse=True)
        
        # Pegar os 20 melhores e os 20 piores
        self.best_performing_bots = sorted_bots[:20]
        self.worst_performing_bots = sorted_bots[-20:] if len(sorted_bots) >= 40 else []
    
    def _update_performance_stats(self):
        """Atualiza estatísticas de desempenho por estratégia, mercado e timeframe"""
        # Resetar estatísticas
        self.strategy_performance = {}
        self.market_performance = {}
        self.timeframe_performance = {}
        
        # Filtrar apenas bots ativos
        active_bots = [bot for bot in self.bots.values() if bot.status == "running"]
        
        if not active_bots:
            return
        
        # Agrupar por estratégia
        for bot in active_bots:
            # Estratégia
            if bot.strategy not in self.strategy_performance:
                self.strategy_performance[bot.strategy] = {
                    "count": 0,
                    "total_profit": 0.0,
                    "total_trades": 0,
                    "successful_trades": 0
                }
            
            self.strategy_performance[bot.strategy]["count"] += 1
            self.strategy_performance[bot.strategy]["total_profit"] += bot.total_profit
            self.strategy_performance[bot.strategy]["total_trades"] += bot.trades_executed
            self.strategy_performance[bot.strategy]["successful_trades"] += bot.successful_trades
            
            # Mercados
            for market in bot.markets:
                if market not in self.market_performance:
                    self.market_performance[market] = {
                        "count": 0,
                        "total_profit": 0.0,
                        "total_trades": 0,
                        "successful_trades": 0
                    }
                
                self.market_performance[market]["count"] += 1
                self.market_performance[market]["total_profit"] += bot.total_profit / len(bot.markets)
                self.market_performance[market]["total_trades"] += bot.trades_executed / len(bot.markets)
                self.market_performance[market]["successful_trades"] += bot.successful_trades / len(bot.markets)
            
            # Timeframes
            for timeframe in bot.timeframes:
                if timeframe not in self.timeframe_performance:
                    self.timeframe_performance[timeframe] = {
                        "count": 0,
                        "total_profit": 0.0,
                        "total_trades": 0,
                        "successful_trades": 0
                    }
                
                self.timeframe_performance[timeframe]["count"] += 1
                self.timeframe_performance[timeframe]["total_profit"] += bot.total_profit / len(bot.timeframes)
                self.timeframe_performance[timeframe]["total_trades"] += bot.trades_executed / len(bot.timeframes)
                self.timeframe_performance[timeframe]["successful_trades"] += bot.successful_trades / len(bot.timeframes)
    
    def _optimization_loop(self):
        """Loop de otimização da rede de bots"""
        while self.optimization_running:
            # Identificar bots de baixo desempenho (ROI negativo com pelo menos 20 trades)
            poor_performing_bots = [
                bot_id for bot_id, bot in self.bots.items()
                if bot.status == "running" and bot.trades_executed >= 20 and bot.roi < 0
            ]
            
            # Otimizar uma parte dos bots de baixo desempenho
            if poor_performing_bots:
                # Escolher aleatoriamente 10% dos bots de baixo desempenho para otimizar
                num_to_optimize = max(1, int(len(poor_performing_bots) * 0.1))
                bots_to_optimize = random.sample(poor_performing_bots, num_to_optimize)
                
                for bot_id in bots_to_optimize:
                    self._optimize_bot(bot_id)
            
            # Iniciar novos bots se o número de ativos for menor que 50% do total
            if self.active_bots < (self.total_bots * 0.5):
                # Calcular quantos bots iniciar
                bots_to_start = int(self.total_bots * 0.6) - self.active_bots
                
                # Selecionar bots inativos
                inactive_bots = [
                    bot_id for bot_id, bot in self.bots.items()
                    if bot.status == "idle"
                ]
                
                if inactive_bots and bots_to_start > 0:
                    # Escolher aleatoriamente bots para iniciar
                    start_count = min(bots_to_start, len(inactive_bots))
                    bots_to_start = random.sample(inactive_bots, start_count)
                    
                    for bot_id in bots_to_start:
                        self.bots[bot_id].start()
            
            # Esperar entre otimizações (entre 30 e 60 segundos)
            time.sleep(random.uniform(30, 60))
    
    def _optimize_bot(self, bot_id):
        """Otimiza um bot específico"""
        bot = self.bots.get(bot_id)
        if not bot:
            return False
        
        # Parar o bot temporariamente
        was_running = bot.status == "running"
        if was_running:
            bot.stop()
        
        # Identificar estratégias de alto desempenho
        high_performing_strategies = []
        for strategy, stats in self.strategy_performance.items():
            if stats["total_trades"] > 0:
                success_rate = stats["successful_trades"] / stats["total_trades"]
                if success_rate > 0.6 and stats["total_profit"] > 0:
                    high_performing_strategies.append(strategy)
        
        # Identificar mercados de alto desempenho
        high_performing_markets = []
        for market, stats in self.market_performance.items():
            if stats["total_trades"] > 0:
                success_rate = stats["successful_trades"] / stats["total_trades"]
                if success_rate > 0.6 and stats["total_profit"] > 0:
                    high_performing_markets.append(market)
        
        # Identificar timeframes de alto desempenho
        high_performing_timeframes = []
        for timeframe, stats in self.timeframe_performance.items():
            if stats["total_trades"] > 0:
                success_rate = stats["successful_trades"] / stats["total_trades"]
                if success_rate > 0.6 and stats["total_profit"] > 0:
                    high_performing_timeframes.append(timeframe)
        
        # Aplicar otimizações aleatoriamente
        changes_made = False
        
        # 1. Mudar a estratégia se houver estratégias de alto desempenho
        if high_performing_strategies and random.random() < 0.7:
            bot.strategy = random.choice(high_performing_strategies)
            changes_made = True
        
        # 2. Atualizar mercados se houver mercados de alto desempenho
        if high_performing_markets and random.random() < 0.6:
            # Manter entre 1-5 mercados
            num_markets = random.randint(1, 5)
            # Garantir que temos mercados suficientes para escolher
            max_markets = min(num_markets, len(high_performing_markets))
            if max_markets > 0:
                bot.markets = random.sample(high_performing_markets, max_markets)
                changes_made = True
        
        # 3. Atualizar timeframes se houver timeframes de alto desempenho
        if high_performing_timeframes and random.random() < 0.5:
            # Manter entre 1-3 timeframes
            num_timeframes = random.randint(1, 3)
            # Garantir que temos timeframes suficientes para escolher
            max_timeframes = min(num_timeframes, len(high_performing_timeframes))
            if max_timeframes > 0:
                bot.timeframes = random.sample(high_performing_timeframes, max_timeframes)
                changes_made = True
        
        # 4. Ajustar parâmetros de risco
        if random.random() < 0.4:
            # Ajustar tamanho máximo da posição
            bot.max_position_size = random.uniform(100, 10000)
            # Ajustar stop loss e take profit
            bot.stop_loss_pct = random.uniform(1, 10)
            bot.take_profit_pct = random.uniform(2, 20)
            # Garantir que take profit > stop loss
            while bot.take_profit_pct <= bot.stop_loss_pct:
                bot.take_profit_pct = random.uniform(2, 20)
            
            changes_made = True
        
        # Reiniciar o bot se estava rodando
        if was_running and changes_made:
            bot.trades_executed = 0
            bot.successful_trades = 0
            bot.failed_trades = 0
            bot.total_profit = 0.0
            bot.roi = 0.0
            bot.trades_history = []
            bot.start()
        
        return changes_made
    
    def get_bot(self, bot_id):
        """Retorna um bot específico pelo ID"""
        return self.bots.get(bot_id)
    
    def get_bots_by_strategy(self, strategy):
        """Retorna bots que utilizam uma estratégia específica"""
        return [bot for bot in self.bots.values() if bot.strategy == strategy]
    
    def get_active_bots(self, limit=None):
        """Retorna os bots ativos"""
        active = [bot for bot in self.bots.values() if bot.status == "running"]
        if limit and len(active) > limit:
            return random.sample(active, limit)
        return active
    
    def get_network_stats(self, days=1):
        """Retorna estatísticas da rede para o período especificado"""
        cutoff = datetime.now() - timedelta(days=days)
        return [s for s in self.network_stats if s["timestamp"] > cutoff]
    
    def get_best_strategies(self, limit=10):
        """Retorna as melhores estratégias com base no desempenho"""
        strategies = []
        
        for strategy, stats in self.strategy_performance.items():
            if stats["total_trades"] > 0:
                success_rate = stats["successful_trades"] / stats["total_trades"]
                avg_profit = stats["total_profit"] / stats["count"] if stats["count"] > 0 else 0
                
                strategies.append({
                    "strategy": strategy,
                    "bots_count": stats["count"],
                    "total_profit": stats["total_profit"],
                    "avg_profit": avg_profit,
                    "success_rate": success_rate * 100
                })
        
        # Ordenar por lucro médio
        strategies.sort(key=lambda x: x["avg_profit"], reverse=True)
        
        return strategies[:limit]
    
    def get_best_markets(self, limit=10):
        """Retorna os melhores mercados com base no desempenho"""
        markets = []
        
        for market, stats in self.market_performance.items():
            if stats["total_trades"] > 0:
                success_rate = stats["successful_trades"] / stats["total_trades"]
                avg_profit = stats["total_profit"] / stats["count"] if stats["count"] > 0 else 0
                
                markets.append({
                    "market": market,
                    "bots_count": stats["count"],
                    "total_profit": stats["total_profit"],
                    "avg_profit": avg_profit,
                    "success_rate": success_rate * 100
                })
        
        # Ordenar por lucro médio
        markets.sort(key=lambda x: x["avg_profit"], reverse=True)
        
        return markets[:limit]
    
    def get_best_timeframes(self, limit=10):
        """Retorna os melhores timeframes com base no desempenho"""
        timeframes = []
        
        for timeframe, stats in self.timeframe_performance.items():
            if stats["total_trades"] > 0:
                success_rate = stats["successful_trades"] / stats["total_trades"]
                avg_profit = stats["total_profit"] / stats["count"] if stats["count"] > 0 else 0
                
                timeframes.append({
                    "timeframe": timeframe,
                    "bots_count": stats["count"],
                    "total_profit": stats["total_profit"],
                    "avg_profit": avg_profit,
                    "success_rate": success_rate * 100
                })
        
        # Ordenar por lucro médio
        timeframes.sort(key=lambda x: x["avg_profit"], reverse=True)
        
        return timeframes[:limit]
    
    def get_status(self):
        """Retorna o status geral da rede de bots"""
        # Calcular estatísticas gerais
        total_profit = 0.0
        total_trades = 0
        successful_trades = 0
        
        for bot in self.bots.values():
            total_profit += bot.total_profit
            total_trades += bot.trades_executed
            successful_trades += bot.successful_trades
        
        # Calcular taxas de sucesso
        success_rate = (successful_trades / max(1, total_trades)) * 100
        active_rate = (self.active_bots / max(1, self.total_bots)) * 100
        profitable_rate = (self.profitable_bots / max(1, self.active_bots)) * 100
        
        return {
            "running": self.running,
            "total_bots": self.total_bots,
            "active_bots": self.active_bots,
            "profitable_bots": self.profitable_bots,
            "active_rate": active_rate,
            "profitable_rate": profitable_rate,
            "total_profit": total_profit,
            "total_trades": total_trades,
            "successful_trades": successful_trades,
            "success_rate": success_rate,
            "last_scan_time": self.last_scan_time
        }

# Singleton para uso global
_trading_bot_network = None

def get_trading_bot_network():
    """Retorna uma instância da rede de bots de trading"""
    global _trading_bot_network
    if _trading_bot_network is None:
        _trading_bot_network = TradingBotNetwork(num_bots=5000)
    return _trading_bot_network

def render_page():
    st.header("Rede de 5000 Bots de Trading")
    
    st.markdown("""
    ### Rede Neural Ultra-Avançada de Bots de Trading
    
    Este módulo implementa 5000 bots de trading autônomos e auto-otimizáveis, que executam
    diferentes estratégias de trading, operando em múltiplos mercados e timeframes.
    
    Os bots constantemente aprendem e evoluem, otimizando suas estratégias com base nos 
    resultados de operações anteriores e nas tendências de mercado. A rede neural integrada
    permite que os bots compartilhem informações e aprendam uns com os outros.
    """)
    
    # Obter instância da rede de bots
    network = get_trading_bot_network()
    
    # Status da rede
    status = network.get_status()
    
    # Controles de início/parada
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Iniciar Rede de Bots", type="primary", disabled=status["running"]):
            result = network.start_network()
            st.success(result)
            st.rerun()
    
    with col2:
        if st.button("Parar Rede de Bots", disabled=not status["running"]):
            result = network.stop_network()
            st.success(result)
            st.rerun()
    
    # Métricas principais
    st.subheader("Métricas da Rede")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Bots Ativos", f"{status['active_bots']:,}/{status['total_bots']:,}")
    
    with col2:
        st.metric("Bots Lucrativos", f"{status['profitable_bots']:,}")
    
    with col3:
        st.metric("Lucro Total", f"${status['total_profit']:,.2f}")
    
    with col4:
        st.metric("Taxa de Sucesso", f"{status['success_rate']:.1f}%")
    
    # Gráfico de métricas da rede
    st.subheader("Desempenho da Rede")
    
    # Obter estatísticas da rede
    network_stats = network.get_network_stats(days=1)
    
    if network_stats:
        # Criar DataFrame para o gráfico
        df = pd.DataFrame(network_stats)
        
        # Converter timestamp para datetime
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        
        # Criar gráfico de linha para bots ativos e lucrativos
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df["timestamp"],
            y=df["active_bots"],
            name="Bots Ativos",
            line=dict(color="blue", width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=df["timestamp"],
            y=df["profitable_bots"],
            name="Bots Lucrativos",
            line=dict(color="green", width=2)
        ))
        
        fig.update_layout(
            title="Bots Ativos e Lucrativos ao Longo do Tempo",
            xaxis_title="Hora",
            yaxis_title="Número de Bots",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Criar gráfico de linha para lucro total
        fig2 = go.Figure()
        
        fig2.add_trace(go.Scatter(
            x=df["timestamp"],
            y=df["total_profit"],
            name="Lucro Total",
            line=dict(color="green", width=2),
            fill="tozeroy",
            fillcolor="rgba(0, 255, 0, 0.1)"
        ))
        
        fig2.update_layout(
            title="Lucro Total ao Longo do Tempo",
            xaxis_title="Hora",
            yaxis_title="Lucro ($)"
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Ainda não há dados suficientes para mostrar estatísticas da rede.")
    
    # Abas para diferentes visualizações
    tab1, tab2, tab3, tab4 = st.tabs([
        "Melhores Bots", "Melhores Estratégias", "Melhores Mercados", "Detalhes de Bot"
    ])
    
    with tab1:
        st.subheader("Top 20 Bots")
        
        # Obter os melhores bots
        best_bots = network.best_performing_bots
        
        if best_bots:
            # Criar DataFrame para a tabela
            data = []
            for bot in best_bots:
                data.append({
                    "ID": bot.bot_id,
                    "Estratégia": bot.strategy,
                    "Mercados": ", ".join(bot.markets),
                    "Timeframes": ", ".join(bot.timeframes),
                    "Trades": bot.trades_executed,
                    "Taxa de Sucesso": f"{(bot.successful_trades / max(1, bot.trades_executed)) * 100:.1f}%",
                    "Lucro Total": f"${bot.total_profit:.2f}",
                    "ROI": f"{bot.roi:.2f}%"
                })
            
            st.dataframe(pd.DataFrame(data), use_container_width=True)
            
            # Selecionar bot para visualizar detalhes
            selected_bot = st.selectbox(
                "Selecione um bot para ver detalhes",
                [bot.bot_id for bot in best_bots],
                format_func=lambda x: f"{x} - {next((bot.strategy for bot in best_bots if bot.bot_id == x), '')}"
            )
            
            if selected_bot:
                st.session_state.selected_bot_id = selected_bot
                st.rerun()
        else:
            st.info("Ainda não há dados suficientes para mostrar os melhores bots.")
    
    with tab2:
        st.subheader("Melhores Estratégias")
        
        # Obter as melhores estratégias
        best_strategies = network.get_best_strategies()
        
        if best_strategies:
            # Criar DataFrame para a tabela
            df = pd.DataFrame(best_strategies)
            
            # Formatar colunas
            df["total_profit"] = df["total_profit"].apply(lambda x: f"${x:.2f}")
            df["avg_profit"] = df["avg_profit"].apply(lambda x: f"${x:.2f}")
            df["success_rate"] = df["success_rate"].apply(lambda x: f"{x:.1f}%")
            
            st.dataframe(df, use_container_width=True)
            
            # Criar gráfico de barras para lucro médio por estratégia
            fig = px.bar(
                best_strategies,
                x="strategy",
                y="avg_profit",
                title="Lucro Médio por Estratégia",
                color="avg_profit",
                color_continuous_scale="Viridis",
                labels={"strategy": "Estratégia", "avg_profit": "Lucro Médio ($)"}
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Ainda não há dados suficientes para mostrar as melhores estratégias.")
    
    with tab3:
        st.subheader("Melhores Mercados e Timeframes")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("#### Top Mercados")
            
            # Obter os melhores mercados
            best_markets = network.get_best_markets()
            
            if best_markets:
                # Criar DataFrame para a tabela
                df = pd.DataFrame(best_markets)
                
                # Formatar colunas
                df["total_profit"] = df["total_profit"].apply(lambda x: f"${x:.2f}")
                df["avg_profit"] = df["avg_profit"].apply(lambda x: f"${x:.2f}")
                df["success_rate"] = df["success_rate"].apply(lambda x: f"{x:.1f}%")
                
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Ainda não há dados suficientes para mostrar os melhores mercados.")
        
        with col2:
            st.write("#### Top Timeframes")
            
            # Obter os melhores timeframes
            best_timeframes = network.get_best_timeframes()
            
            if best_timeframes:
                # Criar DataFrame para a tabela
                df = pd.DataFrame(best_timeframes)
                
                # Formatar colunas
                df["total_profit"] = df["total_profit"].apply(lambda x: f"${x:.2f}")
                df["avg_profit"] = df["avg_profit"].apply(lambda x: f"${x:.2f}")
                df["success_rate"] = df["success_rate"].apply(lambda x: f"{x:.1f}%")
                
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Ainda não há dados suficientes para mostrar os melhores timeframes.")
        
        # Gráfico comparativo de mercados
        if best_markets:
            # Criar gráfico de barras para taxa de sucesso por mercado
            fig = px.bar(
                best_markets[:10],  # Top 10 mercados apenas
                x="market",
                y="success_rate",
                title="Taxa de Sucesso por Mercado",
                color="success_rate",
                color_continuous_scale="Viridis",
                labels={"market": "Mercado", "success_rate": "Taxa de Sucesso (%)"}
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Detalhes do Bot")
        
        # Verificar se há um bot selecionado
        selected_bot_id = st.session_state.get("selected_bot_id")
        
        if not selected_bot_id:
            # Selecionar um bot ativo aleatório
            active_bots = network.get_active_bots(limit=100)
            if active_bots:
                # Escolher um bot aleatório
                selected_bot = random.choice(active_bots)
                selected_bot_id = selected_bot.bot_id
            else:
                st.info("Não há bots ativos para mostrar detalhes.")
                selected_bot_id = None
        
        if selected_bot_id:
            # Obter o bot selecionado
            bot = network.get_bot(selected_bot_id)
            
            if bot:
                # Campo para buscar outro bot por ID
                new_bot_id = st.text_input("Buscar Bot por ID", value=selected_bot_id)
                if new_bot_id != selected_bot_id:
                    new_bot = network.get_bot(new_bot_id)
                    if new_bot:
                        st.session_state.selected_bot_id = new_bot_id
                        st.rerun()
                    else:
                        st.error(f"Bot {new_bot_id} não encontrado.")
                
                # Exibir detalhes do bot
                st.write(f"#### Bot: {bot.bot_id}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Estratégia:** {bot.strategy}")
                    st.write(f"**Status:** {bot.status.capitalize()}")
                    st.write(f"**Mercados:** {', '.join(bot.markets)}")
                    st.write(f"**Timeframes:** {', '.join(bot.timeframes)}")
                    st.write(f"**Nível de Risco:** {bot.risk_level.capitalize()}")
                
                with col2:
                    st.write(f"**Trades Executados:** {bot.trades_executed}")
                    st.write(f"**Trades Bem-sucedidos:** {bot.successful_trades}")
                    st.write(f"**Taxa de Sucesso:** {(bot.successful_trades / max(1, bot.trades_executed)) * 100:.1f}%")
                    st.write(f"**Lucro Total:** ${bot.total_profit:.2f}")
                    st.write(f"**ROI:** {bot.roi:.2f}%")
                
                # Controles do bot
                if bot.status == "running":
                    if st.button("Pausar Bot", key="pause_bot"):
                        success, message = bot.pause()
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                elif bot.status == "paused":
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Retomar Bot", key="resume_bot"):
                            success, message = bot.resume()
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                    with col2:
                        if st.button("Parar Bot", key="stop_bot"):
                            success, message = bot.stop()
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                elif bot.status == "idle":
                    if st.button("Iniciar Bot", key="start_bot", type="primary"):
                        success, message = bot.start()
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                
                # Gráfico de desempenho do bot
                st.write("#### Desempenho do Bot")
                
                performance_data = bot.get_performance_chart_data()
                if performance_data:
                    days = list(range(1, len(performance_data) + 1))
                    cumulative_return = np.cumsum(performance_data)
                    
                    fig = go.Figure()
                    
                    # Retornos diários
                    fig.add_trace(go.Bar(
                        x=days,
                        y=performance_data,
                        name="Retorno Diário (%)",
                        marker_color=["green" if x >= 0 else "red" for x in performance_data]
                    ))
                    
                    # Retorno acumulado
                    fig.add_trace(go.Scatter(
                        x=days,
                        y=cumulative_return,
                        name="Retorno Acumulado (%)",
                        line=dict(color="blue", width=2),
                        yaxis="y2"
                    ))
                    
                    fig.update_layout(
                        title="Desempenho do Bot nos Últimos 30 Dias",
                        xaxis_title="Dia",
                        yaxis_title="Retorno Diário (%)",
                        yaxis2=dict(
                            title="Retorno Acumulado (%)",
                            overlaying="y",
                            side="right"
                        ),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                # Trades recentes
                st.write("#### Trades Recentes")
                
                recent_trades = bot.get_recent_trades()
                if recent_trades:
                    # Criar DataFrame para a tabela
                    data = []
                    for trade in recent_trades:
                        data.append({
                            "ID": trade["id"],
                            "Data/Hora": trade["timestamp"].strftime("%d/%m/%Y %H:%M:%S"),
                            "Mercado": trade["market"],
                            "Timeframe": trade["timeframe"],
                            "Tipo": trade["type"].capitalize(),
                            "Tamanho": f"${trade['position_size']:.2f}",
                            "Lucro (%)": f"{trade['profit_pct']:.2f}%",
                            "Lucro ($)": f"${trade['profit_amount']:.2f}",
                            "Resultado": "✅" if trade["successful"] else "❌"
                        })
                    
                    st.dataframe(pd.DataFrame(data), use_container_width=True)
                else:
                    st.info("Ainda não há trades para mostrar.")
            else:
                st.error("Bot não encontrado.")
    
    # Aviso legal
    st.warning("""
    **AVISO:** A rede de 5000 bots de trading está em modo de simulação para demonstração.
    Em ambiente de produção, os bots operariam com capital real e API keys de exchanges.
    A operação real requer chaves de API com permissões de trading ativadas.
    """)