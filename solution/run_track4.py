from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import sparse
from sklearn.datasets import load_svmlight_file
from sklearn.preprocessing import StandardScaler

from optimization import sgd, sgd_sls
from oracles import StochasticRegressionOracle


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT.parent.parent / "Lab1" / "data" / "bodyfat"
OUTPUT_DIR = ROOT / "output" / "track4"


def load_bodyfat():
    x, y = load_svmlight_file(DATA_PATH)
    scaler = StandardScaler(with_mean=False)
    x = scaler.fit_transform(x).astype(np.float64)
    if sparse.issparse(x):
        x = x.tocsr()
    return x, np.asarray(y, dtype=np.float64).ravel()


def save_convergence(histories, labels):
    plt.figure(figsize=(8, 5))
    for history, label in zip(histories, labels):
        plt.plot(history["epoch"], history["func"], linewidth=2.2, label=label)
    plt.xlabel("Эффективные эпохи")
    plt.ylabel("F(x)")
    plt.yscale("log")
    plt.title("Трек 4: SLS против ручного расписания шага")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    path = OUTPUT_DIR / "track4_convergence.png"
    plt.savefig(path, dpi=180)
    plt.close()
    return path


def save_alpha(history):
    plt.figure(figsize=(8, 5))
    plt.plot(history["epoch"], history["alpha"], linewidth=2.2, color="#b45309")
    plt.xlabel("Эффективные эпохи")
    plt.ylabel("Средний принятый шаг alpha")
    plt.yscale("log")
    plt.title("Трек 4: адаптация длины шага в SLS")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    path = OUTPUT_DIR / "track4_alpha.png"
    plt.savefig(path, dpi=180)
    plt.close()
    return path


def write_summary(rows):
    path = OUTPUT_DIR / "track4_summary.csv"
    with path.open("w", encoding="utf-8") as f:
        f.write("method,final_func,time_sec,final_alpha\n")
        for row in rows:
            f.write("{method},{final_func:.10f},{time_sec:.6f},{final_alpha:.10g}\n".format(**row))
    return path


def main():
    np.random.seed(42)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    x, y = load_bodyfat()
    l2_coef = 1.0 / x.shape[0]
    oracle = StochasticRegressionOracle(x, y, l2_coef=l2_coef)
    x0 = np.zeros(x.shape[1], dtype=np.float64)

    batch_size = 32
    max_epoch = 80

    _, _, manual_history = sgd(
        oracle,
        x0,
        batch_size=batch_size,
        max_epoch=max_epoch,
        lr_schedule="inverse_sqrt",
        lr_params={"alpha_0": 0.01},
        trace=True,
    )

    np.random.seed(42)
    _, _, sls_history = sgd_sls(
        oracle,
        x0,
        batch_size=batch_size,
        max_epoch=max_epoch,
        alpha_0=1.0,
        gamma=0.5,
        rho=1.2,
        c=0.01,
        trace=True,
    )

    convergence_path = save_convergence(
        [manual_history, sls_history],
        ["SGD, лучший ручной inverse sqrt", "SGD + SLS"],
    )
    alpha_path = save_alpha(sls_history)
    summary_path = write_summary([
        {
            "method": "SGD Inverse Sqrt",
            "final_func": manual_history["func"][-1],
            "time_sec": manual_history["time"][-1],
            "final_alpha": 0.01 / np.sqrt(np.ceil(x.shape[0] / batch_size) * max_epoch),
        },
        {
            "method": "SGD + SLS",
            "final_func": sls_history["func"][-1],
            "time_sec": sls_history["time"][-1],
            "final_alpha": sls_history["alpha"][-1],
        },
    ])

    print("dataset=bodyfat, task=Log-Cosh regression")
    print("m={}, n={}, batch_size={}, max_epoch={}".format(
        x.shape[0], x.shape[1], batch_size, max_epoch))
    print("manual_final={:.6f}".format(manual_history["func"][-1]))
    print("sls_final={:.6f}".format(sls_history["func"][-1]))
    print("convergence={}".format(convergence_path))
    print("alpha={}".format(alpha_path))
    print("summary={}".format(summary_path))


if __name__ == "__main__":
    main()
