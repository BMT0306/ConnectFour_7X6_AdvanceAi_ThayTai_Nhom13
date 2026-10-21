"""Base Agent interface for Connect Four AI agents."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Any, Dict
from c4.game.engine import Bitboard


class BaseAgent(ABC):
    """Abstract base class for all Connect Four agents (Levels 1 to 5+).
    
    Unified interface:
      `choose_action(game: Bitboard, budget: Optional[Any] = None) -> int`
    """

    def __init__(self, name: str = "BaseAgent") -> None:
        self.name = name
        self.stats: Dict[str, Any] = {
            "nodes_visited": 0,
            "time_taken": 0.0,
            "depth_reached": 0,
        }

    @abstractmethod
    def choose_action(self, game: Bitboard, budget: Optional[Any] = None) -> int:
        """Selects a legal column [0..6] to play.
        
        Args:
            game: The current Bitboard game state (must not be mutated).
            budget: Optional computational budget (e.g. time limit in seconds,
                    or number of simulations/depth).
                    
        Returns:
            The selected column index (0 to 6).
        """
        pass

    def reset_stats(self) -> None:
        """Resets run-time metrics."""
        self.stats = {
            "nodes_visited": 0,
            "time_taken": 0.0,
            "depth_reached": 0,
        }

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
