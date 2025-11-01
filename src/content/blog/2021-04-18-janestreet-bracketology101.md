---
title: Everyone loves Jane Street
description: Bracketology 101
date: 2021-04-18T00:17:00Z
tags: ["jane-street", "algorithms", "problems"]
draft: false
---

> "The main road is an easy way, but everyone loves the side streets."
> 
> \- Chinese proverb

I recently found out about [Jane Street](https://www.janestreet.com/), a quantitative trading firm which shares new puzzles almost every month that are aimed at challenging one's way of thinking through problems. Quantitative trading has been a passion of mine for a while, and being a puzzle lover myself that enjoys a good challenge, I thought I'd check it out. 
    
## Bracketology 101
This is pasted directly from Jane Street's [page](https://www.janestreet.com/puzzles/bracketology-101-index/).

![](/2021-04-18-janestreet-bracketology101/bracket.png)

> "
> There’s a certain insanity in the air this time of the year that gets us thinking about tournament brackets. Consider a tournament with 16 competitors, seeded 1-16, and arranged in the single-elimination bracket pictured above (identical to a “region” of the NCAA Division 1 basketball tournament). Assume that when the X-seed plays the Y-seed, the X-seed has a Y/(X+Y) probability of winning. E.g. in the first round, the 5-seed has a 12/17 chance of beating the 12-seed.
>
> Suppose the 2-seed has the chance to secretly swap two teams’ placements in the bracket before the tournament begins. So, for example, say they choose to swap the 8- and 16-seeds. Then the 8-seed would play their first game against the 1-seed and have a 1/9 chance of advancing to the next round, and the 16-seed would play their first game against the 9-seed and have a 9/25 chance of advancing.
>
> What seeds should the 2-seed swap to maximize their (the 2-seed’s) probability of winning the tournament, and how much does the swap increase that probability? Give your answer to six significant figures.
> "

## Breaking down the problem

Alright, so the goal is to find a pair of teams that the 2-seed could swap to maximize their odds of winning the tournament.

My first inclination was to do a high-level analysis of the problem. Here's what we know:

- Odds of winning a match are determined by the seeds of the two teams in the match, and are thus independent of the results of any other match
- Therefore, following the equation for the odds of each match, a team's odds of winning the bracket (*if all their opponents are known*) can be defined as a function:
![](/2021-04-18-janestreet-bracketology101/equation.png) 
    - *x* is the team's seed
    - *y<sub>i</sub>* is the seed of the opposing team in round *i*
- The function is maximized when each element is maximized:
    ![](/2021-04-18-janestreet-bracketology101/max_value.png)
- Likewise, the function is minimized when each element is minimized:
    ![](/2021-04-18-janestreet-bracketology101/min_value.png)

So far, we haven't really discovered anything new. Here's a few more quick thoughts:

- The bracket system is setup to favour teams with lower seeds, by increasing the odds that they'll face weaker (higher seeded) teams later in the bracket relative to their opponents.
- Therefore, swapping the 1 and 2 seeds would likely yield a reasonable initial benchmark, since the 1-seed likely has the 'easiest' path in the bracket.  
- If the lower seed wins every game, then the opponents get tougher to beat each round.
    - So, the ideal scenario for any given team is to have the higher seeds as close to them as possible in the bracket.

With all this in consideration, and looking at the original bracket, I suspected that the best option for the 2-seed would be to swap the 3-seed and the 16-seed. This would place the team's two toughest oppponents in the opposing half of the bracket (1 and 3 seeds), and place the weakest team in the tournament in the 2-seed's half, increasing the chances that they would face off (even if still unlikely).

## Calculating the solution
To verify that this is the optimal swap (and calculate the 2-seed's odds), we must run through every possible permutation and calculate the winning odds for the 2-seed for each layout of the bracket. 

To calculate a team's odds of winning the bracket we have to calculate their odds of winning each round:

- First round: g(x, y).
- Second round: they would have two possible opponnents, so we'd multiply the odds of facing each opponent by the team's winning odds against them, and add the two results:
    - g(x, y<sub>A</sub> | y<sub>B</sub>) = g(x, y<sub>A</sub>) * g(y<sub>A</sub>, y<sub>B</sub>) + g(x, y<sub>B</sub>) * g(y<sub>B</sub>, y<sub>A</sub>)
- Third round: repeat the calculations, but this time for four possible opponents, and the odds of them advancing two rounds before losing to our team

and so forth

For example, here's how to calculate the team's odds of winning the original bracket:

- 1st round: 15/(2+15) = 15/17
- 2nd round:
    - Facing 7-seed: 10/17 * 7/9 = 70/153
    - Facing 10-seed: 7/17 * 10/12 = 70/204
    - Total: 70/153 + 70/204 = 243/306
- 3rd round:
    - Facing 6-seed: 11/17 * [14/17 * 3/9 + 3/17 * 14/20] * 6/8 = 2233/11560
    - ...

and so forth

The calculations quickly become very labourious for just a single case. Considering that we have 121 bracket variations (<sup>16</sup>C<sub>2</sub> = 120 possible swaps + the original bracket), clearly we can't solve this by hand.

  
## A little helping script
Rather than going through all these variations by hand, I put on my programmer hat, and came up with a solution to automate the process. 
![](/2021-04-18-janestreet-bracketology101/hackerman.jpg)

It's not particularly clever, but it did the trick nicely.

I defined a `Match` as a tuple of two lists of `Opponent` objects, each representing the teams that would have a chance to play in that match through a side of the bracket. 

An `Opponent` is just a dataclass object, with contains the seed of a team and their odds of reaching the given match.

For each match, we calculate each team's winning odds by repeating the process determined in the previous section:

- for each opponent:
    - calculate the team's odds against that opponent (*Y/(X+Y)*)
    - multiply that by the odds of the opponent reaching that round
    - add to the result (which starts at 0)
- multiply the aggregate result by the team's odds of reaching that round

The two lists of opponents are then merged into one list with updated odds for each team, going into the next match, so the number of lists of teams is halved each round. 

When there is only one list of teams, it means we've played the last match, so the remaining odds represent each team's chances of winning the whole bracket. We check the odds for the 2-seed and update the max odds if there was an improvement.

We then do a swap on the original bracket, and repeat the process. After we've gone through every possible combination, we compute the improvement from the best swap relative to the original bracket.

> **Tip:** I didn't focus on optimisation for this simple problem. I did take one small precaution to avoid swapping any pair of seeds that added to 17 (num_teams + 1). These teams would've already been paired in the original bracket, and swapping them wouldn't change any result.

At the end of this post I'll cover a few of the optimisations that I think would be useful

Finally, we return the difference between the original odds for the 2-seed and the best odds evaluated, and print the number to 6 significant figures.
         
Here's the code:  

```python
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Opponent:
    """
    Store information on a team ahead of the next match
    """
    seed: int
    odds: float


Match = Tuple[List[Opponent], List[Opponent]]


class BracketSolver:
    """
    Determine a team's optimal swap strategy by calculating their odds of 
    winning in every possible permutation of the bracket after one swap
    """
    def __init__(self, num_teams: int) -> None:
        self.num_teams = num_teams
        self.matches: List[Match] = [
            (
                [Opponent(ix+1, 1)], 
                [Opponent(num_teams-ix, 1)]
            ) 
            for ix in range(num_teams // 2)
        ]
        self.bracket = deepcopy(self.matches)

    def __repr__(self) -> str:
        return f'Bracket(num_teams={self.num_teams})'
    
    def __str__(self) -> str:
        return str('\n'.join([str(match) for match in self.matches]))
    
    def swap(self, seed1: int, seed2: int) -> None:
        """
        Swap two teams
        :param seed1: first seed to swap
        :param seed2: second seed to swap
        """
        seen = 0
        self.matches = deepcopy(self.bracket)
        
        for match in self.matches:
            for opponent_list in match:
                if opponent_list[0].seed == seed1:
                    opponent_list[0].seed = seed2
                    seen += 1
                elif opponent_list[0].seed == seed2:
                    opponent_list[0].seed = seed1
                    seen += 1
                    
                if seen >= 2:
                    return
           
    def calculate_team_odds(self, seed, opponents: List[Opponent]) -> float:
        """
        Calculate odds of a given team winning the round against a set of opponents
        :param seed: team seed
        :param opponents: list of opponents, each defined by their seed and their odds of making to the current stage
        :return: odds of the given seed winning the round ([0,1])
        """
        return sum(
            opp.odds * opp.seed / (opp.seed + seed) 
            for opp in opponents
        )
        
    def calculate_match_odds(self, left_opponents: List[Opponent], right_opponents: List[Opponent]) -> List[Opponent]:
        """
        Each match is defined by two lists of opponents, one from each side of the bracket that led to that match.
        The odds of any team making it to the next stage are the sum of the odds of each opponent in the opposite 
        list reaching that round and losing to them, multiplied by their own odds of reaching that round
        :return: list of each team in the match and their odds of reaching the next round
        """
        result: List[Opponent] = []
        
        bracket = [left_opponents, right_opponents]
        for ix, (teams, opponents) in enumerate(zip(bracket, reversed(bracket))):
            result += [
                Opponent(
                    seed=team.seed,
                    odds=team.odds*self.calculate_team_odds(seed=team.seed, opponents=opponents)
                )
                for team in teams
            ]

        return result
        
    def play_matches(self) -> List[Opponent]:
        """
        Play all matches in the current round, and produce pairings for the next round.
        :return: odds of each team making it to the next round
        """
        team_odds = [
            self.calculate_match_odds(
                left_opponents=left_opponents,
                right_opponents=right_opponents
            )
            for left_opponents, right_opponents in self.matches
        ]

        self.matches = [] if len(team_odds) == 1 else [
            (team_odds[ix], team_odds[-(ix+1)]) 
            for ix in range(len(team_odds) // 2)
        ]
        
        return team_odds
        
                
    def calculate_odds(self, seed: int) -> float:
        """
        Calculate a given team's (represented by their seed) odds of winning the current bracket
        :param seed: seed of the team whose odds to calculate
        :return: odds ([0,1])
        """
        if not self.matches:
            self.matches = deepcopy(self.bracket)
            
        while self.matches:
            team_odds = self.play_matches()[0]
            
        for team in team_odds:
            if team.seed == seed:
                return team.odds
            
    def __call__(self, seed: int) -> float:
        """
        Determine which swap produces the optimal odds of a given team winning
        :param seed: seed of the team to maximize odds for
        :return: increase in winning odds for the given team compared to the original bracket
        """
        original_odds = self.calculate_odds(seed=seed)
        best_odds = original_odds
        
        # No swap, by default, represented as swapping the team with itself
        swap = (seed, seed)
        
        print(f"Original odds: {original_odds}")
        
        for seed1 in range(1, self.num_teams+1):
            for seed2 in range(seed1+1, self.num_teams+1):
                # Skip swapping teams that are facing each other in the first round
                if seed1 + seed2 == self.num_teams + 1:
                    continue
                    
                self.swap(seed1, seed2)
                new_odds = self.calculate_odds(seed=seed)
                if new_odds > best_odds:
                    swap = (seed1, seed2)
                    best_odds = new_odds
                    print(f"New best_odd: {100*best_odds:.2f}% {swap}")

        print(f"Best odds of {100*best_odds:.2f}% ({best_odds}) with swap = {swap}")
                    
        return best_odds-original_odds
    
bracket = BracketSolver(num_teams=16)
print(f"{bracket(seed=2):.6f}")
```


### Results
Here's the output of running this solver:
```python
>>> Original odds: 0.21603968781701657
>>> New best_odd: 23.03% (1, 2)
>>> New best_odd: 23.43% (1, 12)
>>> New best_odd: 23.67% (1, 13)
>>> New best_odd: 23.97% (1, 14)
>>> New best_odd: 26.03% (3, 8)
>>> New best_odd: 26.23% (3, 9)
>>> New best_odd: 28.16% (3, 16)
>>> Best odds of 28.16% (0.2816191915195931) with swap = (3, 16)
>>> 0.065580
```

It seems our expectation was correct, the optimal swap was replacing the 3-seed with the 16-seed! 

### Optimisation
I focused first on producing a working solution, expecting to have some efficiency concerns due to the exponential growth in calculations with each round. It turns out that it ran pretty quickly for a 16-team/4 round bracket. Since the code was all parameterised, I briefly played around with larger brackets:

```python
# for reference
%timeit BracketSolver(num_teams=16)(seed=2)
...
>>> Best odds of 28.16% (0.2816191915195931) with swap = (3, 16)
>>> 76 ms ± 3.07 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
```

```python
%timeit BracketSolver(num_teams=32)(seed=2)
...
>>> Best odds of 28.53% (0.2853359913167945) with swap = (3, 32)
>>> 765 ms ± 69.7 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

```python
%timeit BracketSolver(num_teams=64)(seed=2)
...
>>> Best odds of 28.72% (0.28716568501254636) with swap = (3, 64)
>>> 6.71 s ± 319 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

```python
%timeit BracketSolver(num_teams=128)(seed=2)
...
>>> Best odds of 28.81% (0.28808790218275504) with swap = (3, 128)
>>> 1min 36s ± 2.49 s per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

We can also observe that our original thesis of swapping the 3-seed with the lowest seed seems holds true for larger brackets as well!

The performance only started to take a toll with a 64-team bracket onwards, but the decay in performance followed an exponential trend (about 10x!) everytime the bracket size was increased.
If I were to improve this solution, I would consider the following approaches:

1. [Memoization](https://en.wikipedia.org/wiki/Memoization#:~:text=In%20computing%2C%20memoization%20or%20memoisation,the%20same%20inputs%20occur%20again.) - with only one swap allowed, all bracket variations are nearly identical to the original bracket. As such, the results of each match in the original bracket could be saved in a dictionary, indexed by the list of opponents that take part in each side, and can be referenced later when the same match is played in another variation of the bracket 
2. Intermediate checks - after each round, if the 2-seed's odds are already lower than the current best odds, skip ahead to the next variation
3. Swap (3-seed, last seed) first. To make the intermediate checks more aggressive, start by calculating what we assume to be the best swap beforehand
4. Calculate only the 2-seed's odd in the last match - the other ones are irrelevant at the last stage
5. Discard the 2-seed's opponents after each round. After the 2-seed defeats an opponent, the loser of the match cannot impact the bracket anymore
6. Disregard any swaps that don't change the round at which the 2-seed would face either of the swapped opponents
    - ok, this is more of a theory that I would be curious to test, but I suspect that swapping opponents while keeping their relative distance to another team doesn't affect their winning chances considerably. This is because we miss out on the opportunity to send a tough opponent to the other side of the bracket, making them compete with all the other strong opponents on the side for a chance at the title. If we swap opponents but don't alter the overall set of teams anyone would have to face before contesting the 2-seed, it suggests to me that the impact of the swap would be greatly diminished.
    - e.g: swapping the 5 and 13 seeds. It doesn't really do much: seeds 4-5 would still be strong favourites to win the first two rounds over 12-13, and would then play the winner of 1-8-9-16, for a chance at the final.
    - would love to hear other thoughts on this, if anyone is curious to pick up this exercise!
    - at any rate, if we could act on this theory, we'd eliminate just over 46% of the variations to evaluate, in the first place (121 -> 65)
7. It would also be worth reducing the space complexity by reutilising `Opponent` objects instead of creating new ones each round
8. Swapping two teams could also be done more efficiently:
    - instead of deep copying the original bracket everytime we want to swap, we could just revert the previous swap (by redoing it), and reuse the previous bracket
    - instead of iterating through all teams in the bracket looking for the seed we want to swap, we could index the list directly:
        
      ```python
      def swap(self, seed1: int, seed2: int) -> None:
          """..."""
          seeds = [seed1, seed2]
          ixs = [min(seed, self.num_teams+1-seed)-1 for seed in seeds]
          for ix, seed, new_seed in zip(ixs, seeds, reversed(seeds)):
              # the lower seed comes first in the match 
              index_in_match = seed > self.num_teads / 2
              self.matches[ix][index_in_match].seed = new_seed 
      ```

That's my take on the latest puzzle by Jane Street! Looking forward to trying out the next challenges! 