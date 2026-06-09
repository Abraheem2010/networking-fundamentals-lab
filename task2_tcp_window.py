"""Task 2 - TCP congestion control (AIMD) simulation.

Simulates the Additive-Increase / Multiplicative-Decrease behaviour of a TCP
congestion window over a number of RTT rounds, with random loss events.
"""
import random


def trial_loss(loss_prob, rng):
    """
    return True if a loss event occurs this RTT (Bernoulli with loss_prob)
    """
    return rng.random() < loss_prob


def aimd_step(cwnd_mss, loss_happened):
    """
    apply AIMD:
    - if loss_happened: halve cwnd (min 1)
    - else: cwnd += 1
    return new_cwnd_mss (int or float)
    """
    if loss_happened:
        new_cwnd_mss = max(1, cwnd_mss / 2)  # Halve cwnd, min 1
    else:
        new_cwnd_mss = cwnd_mss + 1  # Increase cwnd by 1
    return new_cwnd_mss


def simulate_aimd(rounds, loss_prob=0.2, seed=None, start_mss=1, verbose=True):
    """
    run 'rounds' RTTs, optionally print cwnd each RTT,
    and return the list of cwnd values (one per round)
    """
    rng = random.Random(seed)  # Initialize random number generator with seed
    cwnd_mss = start_mss  # Start with initial congestion window size
    history = []
    for round in range(rounds):
        loss_happened = trial_loss(loss_prob, rng)  # Determine if loss occurs
        cwnd_mss = aimd_step(cwnd_mss, loss_happened)  # Update congestion window
        history.append(cwnd_mss)
        if verbose:
            print(f"Round {round + 1}: cwnd = {cwnd_mss:.2f} MSS")  # Print current cwnd
    return history


if __name__ == "__main__":
    # Example:
    simulate_aimd(rounds=50, loss_prob=0.2, seed=42, start_mss=1)
