"""Simulation comparator for testing deck variations."""

from typing import List, Dict, Any
from dataclasses import dataclass, field
import statistics


@dataclass
class SimulationResult:
    """Result of a single simulation."""
    version: str
    player_id: int
    player_name: str
    life_total: int
    turns_survived: int
    damage_dealt: int
    damage_taken: int
    cards_drawn: int
    commanders_cast: int
    won: bool
    key_card_played: str = ""


@dataclass
class VersionStats:
    """Statistics for a deck version."""
    version_name: str
    total_simulations: int = 0
    wins: int = 0
    losses: int = 0
    win_rate: float = 0.0
    avg_life_total: float = 0.0
    avg_turns_survived: float = 0.0
    avg_damage_dealt: float = 0.0
    avg_damage_taken: float = 0.0
    avg_cards_drawn: float = 0.0
    key_cards_used: Dict[str, int] = field(default_factory=dict)
    results: List[SimulationResult] = field(default_factory=list)

    def add_result(self, result: SimulationResult) -> None:
        """Add a simulation result.
        
        Args:
            result: SimulationResult to add
        """
        self.results.append(result)
        self.total_simulations += 1
        
        if result.won:
            self.wins += 1
        else:
            self.losses += 1
        
        if result.key_card_played:
            self.key_cards_used[result.key_card_played] = \
                self.key_cards_used.get(result.key_card_played, 0) + 1

    def calculate_stats(self) -> None:
        """Calculate aggregated statistics."""
        if not self.results:
            return
        
        self.win_rate = (self.wins / self.total_simulations) * 100
        self.avg_life_total = statistics.mean([r.life_total for r in self.results])
        self.avg_turns_survived = statistics.mean([r.turns_survived for r in self.results])
        self.avg_damage_dealt = statistics.mean([r.damage_dealt for r in self.results])
        self.avg_damage_taken = statistics.mean([r.damage_taken for r in self.results])
        self.avg_cards_drawn = statistics.mean([r.cards_drawn for r in self.results])

    def __str__(self) -> str:
        return f"VersionStats({self.version_name}, {self.win_rate:.1f}% win rate)"


class SimulationComparator:
    """Compares two deck versions across multiple simulations."""

    def __init__(self, version_a_name: str, version_b_name: str, num_sims: int = 5):
        """Initialize comparator.
        
        Args:
            version_a_name: Name of version A
            version_b_name: Name of version B
            num_sims: Number of simulations per version
        """
        self.version_a_name = version_a_name
        self.version_b_name = version_b_name
        self.num_sims = num_sims
        self.version_a_stats = VersionStats(version_a_name)
        self.version_b_stats = VersionStats(version_b_name)

    def add_simulation_result(self, result: SimulationResult) -> None:
        """Add a simulation result.
        
        Args:
            result: SimulationResult to add
        """
        if result.version == "A":
            self.version_a_stats.add_result(result)
        elif result.version == "B":
            self.version_b_stats.add_result(result)

    def finalize_stats(self) -> None:
        """Finalize statistics calculation."""
        self.version_a_stats.calculate_stats()
        self.version_b_stats.calculate_stats()

    def get_comparison_report(self) -> str:
        """Generate a comparison report.
        
        Returns:
            Formatted comparison report
        """
        self.finalize_stats()
        
        report = []
        report.append("\n" + "="*70)
        report.append("📊 DECK COMPARISON REPORT")
        report.append("="*70)
        report.append(f"Simulations per version: {self.num_sims}\n")
        
        # Win Rate Comparison
        report.append("🏆 WIN RATE")
        report.append("-" * 70)
        report.append(f"  Version A ({self.version_a_name}): {self.version_a_stats.win_rate:.1f}% ({self.version_a_stats.wins}/{self.version_a_stats.total_simulations})")
        report.append(f"  Version B ({self.version_b_name}): {self.version_b_stats.win_rate:.1f}% ({self.version_b_stats.wins}/{self.version_b_stats.total_simulations})")
        
        win_diff = self.version_a_stats.win_rate - self.version_b_stats.win_rate
        if win_diff > 0:
            report.append(f"  ✅ Version A is {abs(win_diff):.1f}% better\n")
        elif win_diff < 0:
            report.append(f"  ✅ Version B is {abs(win_diff):.1f}% better\n")
        else:
            report.append(f"  ⚖️  Both versions tied\n")
        
        # Life Total Comparison
        report.append("❤️  AVERAGE LIFE TOTAL")
        report.append("-" * 70)
        report.append(f"  Version A: {self.version_a_stats.avg_life_total:.1f}")
        report.append(f"  Version B: {self.version_b_stats.avg_life_total:.1f}")
        life_diff = self.version_a_stats.avg_life_total - self.version_b_stats.avg_life_total
        report.append(f"  Difference: {life_diff:+.1f} life\n")
        
        # Turns Survived Comparison
        report.append("⏱️  AVERAGE TURNS SURVIVED")
        report.append("-" * 70)
        report.append(f"  Version A: {self.version_a_stats.avg_turns_survived:.1f}")
        report.append(f"  Version B: {self.version_b_stats.avg_turns_survived:.1f}")
        turns_diff = self.version_a_stats.avg_turns_survived - self.version_b_stats.avg_turns_survived
        report.append(f"  Difference: {turns_diff:+.1f} turns\n")
        
        # Damage Comparison
        report.append("⚔️  DAMAGE DEALT")
        report.append("-" * 70)
        report.append(f"  Version A: {self.version_a_stats.avg_damage_dealt:.1f} avg")
        report.append(f"  Version B: {self.version_b_stats.avg_damage_dealt:.1f} avg")
        dmg_diff = self.version_a_stats.avg_damage_dealt - self.version_b_stats.avg_damage_dealt
        report.append(f"  Difference: {dmg_diff:+.1f} damage\n")
        
        # Damage Taken Comparison
        report.append("🛡️  DAMAGE TAKEN")
        report.append("-" * 70)
        report.append(f"  Version A: {self.version_a_stats.avg_damage_taken:.1f} avg")
        report.append(f"  Version B: {self.version_b_stats.avg_damage_taken:.1f} avg")
        def_diff = self.version_a_stats.avg_damage_taken - self.version_b_stats.avg_damage_taken
        report.append(f"  Difference: {def_diff:+.1f} damage\n")
        
        # Cards Drawn Comparison
        report.append("🎴 CARDS DRAWN")
        report.append("-" * 70)
        report.append(f"  Version A: {self.version_a_stats.avg_cards_drawn:.1f} avg")
        report.append(f"  Version B: {self.version_b_stats.avg_cards_drawn:.1f} avg")
        cards_diff = self.version_a_stats.avg_cards_drawn - self.version_b_stats.avg_cards_drawn
        report.append(f"  Difference: {cards_diff:+.1f} cards\n")
        
        # Key Cards Used
        if self.version_a_stats.key_cards_used or self.version_b_stats.key_cards_used:
            report.append("🔑 KEY CARDS USAGE")
            report.append("-" * 70)
            report.append(f"  Version A:")
            for card, count in sorted(self.version_a_stats.key_cards_used.items(), key=lambda x: x[1], reverse=True):
                report.append(f"    - {card}: {count}x")
            report.append(f"  Version B:")
            for card, count in sorted(self.version_b_stats.key_cards_used.items(), key=lambda x: x[1], reverse=True):
                report.append(f"    - {card}: {count}x")
            report.append()
        
        # Recommendation
        report.append("\n" + "="*70)
        report.append("💡 RECOMMENDATION")
        report.append("="*70)
        
        if self.version_a_stats.win_rate > self.version_b_stats.win_rate + 5:
            report.append(f"✅ Version A ({self.version_a_name}) is significantly better!")
        elif self.version_b_stats.win_rate > self.version_a_stats.win_rate + 5:
            report.append(f"✅ Version B ({self.version_b_name}) is significantly better!")
        else:
            report.append("⚖️  Both versions are competitive. Choose based on playstyle preference.")
        
        report.append("="*70 + "\n")
        
        return "\n".join(report)

    def get_detailed_results(self) -> str:
        """Get detailed results for each simulation.
        
        Returns:
            Detailed results string
        """
        details = []
        details.append("\n📋 DETAILED SIMULATION RESULTS\n")
        
        details.append(f"VERSION A ({self.version_a_name}):")
        details.append("-" * 70)
        for i, result in enumerate(self.version_a_stats.results, 1):
            status = "✅ WIN" if result.won else "❌ LOSS"
            details.append(f"  Sim {i}: {status} | Life: {result.life_total} | Turns: {result.turns_survived} | DMG Out: {result.damage_dealt} | DMG In: {result.damage_taken}")
        
        details.append(f"\nVERSION B ({self.version_b_name}):")
        details.append("-" * 70)
        for i, result in enumerate(self.version_b_stats.results, 1):
            status = "✅ WIN" if result.won else "❌ LOSS"
            details.append(f"  Sim {i}: {status} | Life: {result.life_total} | Turns: {result.turns_survived} | DMG Out: {result.damage_dealt} | DMG In: {result.damage_taken}")
        
        details.append("\n")
        return "\n".join(details)
