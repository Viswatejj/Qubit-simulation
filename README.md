# Qubit Simulator

A command-line quantum computing simulator written in Python. Create qubits, apply single-, two- and three-qubit gates, watch single qubits move around an interactive 3D Bloch sphere, and inspect the combined multi-qubit state as amplitudes and probabilities.

Everything lives in one file: `Qubit.py`.

## Features

- Create qubits in |0>, |1>, or any custom normalised state (`alpha|0> + beta|1>`)
- 9 single-qubit gates
- 12 two-qubit gates and 10 three-qubit gates
- Interactive Bloch sphere (matplotlib) that redraws as you apply gates
- Combined system view using the Kronecker (tensor) product, listing every basis state with its amplitude and probability

## Requirements

- Python **3.10 or newer** (the program uses `match` statements)
- [numpy](https://numpy.org/)
- [matplotlib](https://matplotlib.org/) with a GUI backend (the Bloch sphere opens in an interactive window)

```bash
pip install numpy matplotlib
```

## Running

```bash
python Qubit.py
```

A Bloch sphere window opens and the main menu appears in the terminal.

## Menu

```
1. Create a qubit
2. Apply gate to singular qubit
3. Display a qubit in a bloch sphere
4. Display the Total qubit system
5. Perform operations on the total qubit system
q. Quit
```

| Option | What it does |
|---|---|
| **1** | Creates a new qubit as \|0>, \|1> or a custom state. Custom values are entered as Python complex numbers (e.g. `0.7071`, `0.7071j`, `1+2j`, no spaces) and must satisfy \|alpha\|² + \|beta\|² = 1. |
| **2** | Picks a qubit and applies one single-qubit gate to it. Prints the new state and probabilities and redraws the Bloch sphere. |
| **3** | Draws a chosen qubit on the Bloch sphere. |
| **4** | Needs at least 2 qubits. Prints the combined state of all qubits in the register. |
| **5** | Applies gates to the combined state. The number of qubits in the register must exactly match the system size you choose (2 or 3). |

### Option 5 in detail

After choosing a 2- or 3-qubit system, you can repeatedly:

1. **Apply a single-qubit gate to all qubits**: the chosen gate is applied to every qubit at once (built as `G ⊗ G ⊗ ...`)
2. **Apply a multi-qubit gate** from the 2- or 3-qubit gate list

Each step prints the updated amplitudes and probabilities. Enter `q` to go back to the main menu.

> **Note:** option 5 works on a temporary copy of the combined state. The individual qubits stored in the register are not changed, and the combined state is rebuilt from them the next time you enter option 4 or 5.

## Gates

### Single-qubit

Identity, Pauli X, Pauli Y, Pauli Z, Hadamard, S, T, S†, T†

### Two-qubit

CNOT, CNOT01 (control and target reversed), Controlled Identity, Controlled Pauli X / Y / Z, Controlled Hadamard, Controlled S, Controlled T, SWAP, Controlled S†, Controlled T†

### Three-qubit

Identity, Toffoli (CCX), CC-Pauli Y, CCZ, CC-Hadamard, CC-S, CC-S†, CC-T, CC-T†, Controlled SWAP (Fredkin)

## Conventions

- **Qubit ordering:** qubit 1 is the leftmost (most significant) qubit in the combined state, so for two qubits the basis order is |00>, |01>, |10>, |11>.
- **Controls:** in controlled gates, qubit 1 is the control (CNOT01 reverses this for two qubits). In Controlled SWAP, qubit 1 controls the swap of qubits 2 and 3.
- **Bloch vector:** computed from the relative amplitudes, with `theta = 2·arccos(|alpha|)` and `phi = arg(beta) - arg(alpha)`. Global phase is ignored, as expected.

## Example session

Create two qubits and entangle them into a Bell state:

1. Menu `1` → `1` to create qubit #1 in |0>
2. Menu `1` → `1` to create qubit #2 in |0>
3. Menu `2` → qubit `1` → gate `5` (Hadamard) on qubit 1 (note that this changes the qubit itself)
4. Menu `5` → `1` (2 qubits) → option `2` → gate `1` (CNOT)

Expected output for the final state:

```
|00>  amplitude (0.707+0j)   probability 0.500
|01>  amplitude 0j           probability 0.000
|10>  amplitude 0j           probability 0.000
|11>  amplitude (0.707+0j)   probability 0.500
```

## Code overview

| Section | Contents |
|---|---|
| Gate matrices | Base states `ket0`, `ket1` and all 1-, 2- and 3-qubit gate matrices as complex numpy arrays |
| Classes | `qubitState` (the state vector, probabilities and `apply`), `qubitRegister` (list of all qubits), `qubit` (a single qubit; every new one is added to the shared `qubit.register`) |
| `kroneckerProduct()` | Combines every qubit in the register into one state vector using `np.kron` |
| Gate dictionaries | `singleGates`, `multiGates`, `threeGates` map menu numbers to `(name, matrix)` |
| Bloch sphere | `blochVector()` converts a state to (x, y, z); `draw_bloch()` renders the sphere, axes and state arrow |
| `showState()` | Prints a multi-qubit state as basis labels with amplitudes and probabilities |
| Main loop | The menu-driven `while True` loop with a `match` statement per option |

## Known limitations

- Quantum state is stored as separate per-qubit vectors, so **entangled states can't be saved back to individual qubits**. Entanglement only exists inside option 5's temporary combined state.
- The Bloch sphere only represents a single, unentangled qubit.
- Entering `q` at the gate prompt in option 2 exits the whole program rather than returning to the main menu.
- Qubit-number prompts use `int(input(...))` with no range check, so invalid input raises an error.
- Gates in option 5 always act on the whole system; there is no way to target a chosen subset of qubits (for example, a Hadamard on only one qubit of three).
- Some gate matrices are duplicates (e.g. `Gate_CNOT` and `Gate_CpauliX`), which is harmless but redundant.

## Possible next steps

- Apply multi-qubit gates to chosen qubits within a larger register
- Measurement with random collapse
- Input validation and a "back" option in every sub-menu
- Save and load circuits
