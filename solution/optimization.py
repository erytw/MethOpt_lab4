import numpy as np
from time import time


def _init_history(trace, oracle, x, start_time):
    if not trace:
        return None
    return {
        'epoch': [0.0],
        'func': [oracle.func(x)],
        'time': [time() - start_time],
    }


def _save_history(history, oracle, x, epoch, start_time):
    if history is None:
        return
    history['epoch'].append(float(epoch))
    history['func'].append(oracle.func(x))
    history['time'].append(time() - start_time)


def _learning_rate(lr_schedule, lr_params, iteration, epoch):
    alpha_0 = lr_params.get('alpha_0', 0.01)

    if lr_schedule == 'constant':
        return alpha_0
    if lr_schedule == 'inverse_sqrt':
        return alpha_0 / np.sqrt(iteration + 1)
    if lr_schedule == 'step_decay':
        gamma = lr_params.get('gamma', 0.5)
        drop_freq = lr_params.get('drop_freq', 10)
        return alpha_0 * (gamma ** (int(epoch) // drop_freq))

    raise ValueError("Unknown lr_schedule: {}".format(lr_schedule))


def _check_batch_size(batch_size, oracle):
    batch_size = int(batch_size)
    if batch_size <= 0:
        raise ValueError('batch_size must be positive')
    return min(batch_size, oracle.m)


def sgd(oracle, x_0, batch_size=128, max_epoch=100, 
        lr_schedule='constant', lr_params=None,
        trace=False, display=False):
    """
    Метод стохастического градиентного спуска (Mini-batch SGD).

    Parameters
    ----------
    oracle : BaseStochasticOracle
        Оракул с методами .func() и .grad()
    x_0 : np.array
        Начальная точка.
    batch_size : int
        Размер мини-батча.
    max_epoch : int
        Максимальное число эффективных эпох (1 эпоха = m вычислений градиента).
    lr_schedule : str
        Стратегия выбора шага: 'constant', 'inverse_sqrt', 'step_decay'.
    lr_params : dict
        Словарь параметров для стратегии выбора шага.
        Например: {'alpha_0': 0.1, 'gamma': 0.5, 'drop_freq': 10}
    trace : bool
        Если True, сохранять историю сходимости.
    display : bool
        Если True, выводить логи.

    Returns
    -------
    x_star : np.array
        Найденная точка.
    message : string
        'success'
    history : dict or None
        Словарь с историей:
        - history['epoch'] : list of floats (число эффективных эпох)
        - history['func'] : list of floats (значение функции на ВСЕЙ выборке)
        - history['time'] : list of floats (время в секундах)
    """
    if lr_params is None:
        lr_params = {'alpha_0': 0.01}
    
    x = np.asarray(x_0, dtype=float).copy()
    batch_size = _check_batch_size(batch_size, oracle)
    start_time = time()
    history = _init_history(trace, oracle, x, start_time)
    iteration = 0

    for epoch in range(int(max_epoch)):
        samples_seen = 0

        while samples_seen < oracle.m:
            current_batch_size = min(batch_size, oracle.m - samples_seen)
            batch_idx = np.random.choice(
                oracle.m, current_batch_size, replace=False)
            g_k = oracle.grad(x, batch_idx)
            alpha_k = _learning_rate(lr_schedule, lr_params, iteration, epoch)
            x -= alpha_k * g_k
            iteration += 1
            samples_seen += current_batch_size

        _save_history(history, oracle, x, epoch + 1, start_time)
        if display:
            print('Epoch: {}, func: {:.6e}'.format(epoch + 1, oracle.func(x)))

    return x, 'success', history


def sgd_sls(oracle, x_0, batch_size=128, max_epoch=100, alpha_0=1.0,
            gamma=0.5, rho=1.1, c=0.1, max_ls_iter=20,
            trace=False, display=False):
    """
    SGD со стохастическим линейным поиском по условию Армихо на мини-батче.

    На каждой итерации батч фиксируется на все время бэктрекинга:
        f_I(x - alpha * grad f_I(x)) <= f_I(x) - c * alpha * ||grad f_I(x)||^2.

    history дополнительно содержит:
        - history['alpha'] : средний принятый шаг за эпоху
    """
    x = np.asarray(x_0, dtype=float).copy()
    batch_size = _check_batch_size(batch_size, oracle)
    start_time = time()
    history = _init_history(trace, oracle, x, start_time)
    if history is not None:
        history['alpha'] = [float(alpha_0)]

    alpha = float(alpha_0)

    for epoch in range(int(max_epoch)):
        samples_seen = 0
        epoch_alphas = []

        while samples_seen < oracle.m:
            current_batch_size = min(batch_size, oracle.m - samples_seen)
            batch_idx = np.random.choice(
                oracle.m, current_batch_size, replace=False)

            g_k = oracle.grad(x, batch_idx)
            grad_norm_sq = float(np.dot(g_k, g_k))
            f_current = oracle.func(x, batch_idx)
            trial_alpha = alpha * rho

            if grad_norm_sq > 0.0:
                for _ in range(int(max_ls_iter)):
                    x_trial = x - trial_alpha * g_k
                    f_trial = oracle.func(x_trial, batch_idx)
                    armijo_rhs = f_current - c * trial_alpha * grad_norm_sq
                    if f_trial <= armijo_rhs:
                        break
                    trial_alpha *= gamma

            x -= trial_alpha * g_k
            alpha = trial_alpha
            epoch_alphas.append(alpha)
            samples_seen += current_batch_size

        _save_history(history, oracle, x, epoch + 1, start_time)
        if history is not None:
            history['alpha'].append(float(np.mean(epoch_alphas)))
        if display:
            print('Epoch: {}, func: {:.6e}, alpha: {:.3e}'.format(
                epoch + 1, oracle.func(x), np.mean(epoch_alphas)))

    return x, 'success', history


def svrg(oracle, x_0, step_size=0.01, batch_size=128, max_epoch=100, 
         trace=False, display=False):
    """
    Stochastic Variance Reduced Gradient (SVRG).

    Parameters
    ----------
    oracle : BaseStochasticOracle
        Оракул с методами .func() и .grad()
    x_0 : np.array
        Начальная точка.
    step_size : float
        Постоянный размер шага (alpha).
    batch_size : int
        Размер мини-батча для внутреннего цикла.
    max_epoch : int
        Максимальное число эффективных эпох.
        Внимание: вычисление полного градиента стоит 1 эпоху!

    Returns
    -------
    x_star : np.array
    message : string
    history : dict or None
    """
    x = np.asarray(x_0, dtype=float).copy()
    batch_size = _check_batch_size(batch_size, oracle)
    start_time = time()
    history = _init_history(trace, oracle, x, start_time)
    effective_epoch = 0

    while effective_epoch < int(max_epoch):
        x_tilde = x.copy()
        full_grad = oracle.grad(x_tilde)
        effective_epoch += 1
        _save_history(history, oracle, x, effective_epoch, start_time)
        if display:
            print('Epoch: {}, func: {:.6e}'.format(
                effective_epoch, oracle.func(x)))

        if effective_epoch >= int(max_epoch):
            break

        samples_seen = 0
        while samples_seen < oracle.m:
            current_batch_size = min(batch_size, oracle.m - samples_seen)
            batch_idx = np.random.choice(
                oracle.m, current_batch_size, replace=False)
            g_stoch = oracle.grad(x, batch_idx)
            g_tilde = oracle.grad(x_tilde, batch_idx)
            g_k = g_stoch - g_tilde + full_grad
            x -= step_size * g_k
            samples_seen += current_batch_size

        effective_epoch += 1
        _save_history(history, oracle, x, effective_epoch, start_time)
        if display:
            print('Epoch: {}, func: {:.6e}'.format(
                effective_epoch, oracle.func(x)))

    return x, 'success', history


def adam(oracle, x_0, step_size=0.001, batch_size=128, max_epoch=100, 
         beta1=0.9, beta2=0.999, eps=1e-8, trace=False, display=False):
    """
    Адаптивный метод Adam.

    Parameters
    ----------
    oracle : BaseStochasticOracle
        Оракул с методами .func() и .grad()
    x_0 : np.array
        Начальная точка.
    step_size : float
        Базовый размер шага (alpha).
    batch_size : int
        Размер мини-батча.
    max_epoch : int
        Максимальное число эффективных эпох.
    beta1, beta2 : float
        Коэффициенты экспоненциального сглаживания.
    eps : float
        Константа для стабильности деления.

    Returns
    -------
    x_star : np.array
    message : string
    history : dict or None
    """
    x = np.asarray(x_0, dtype=float).copy()
    batch_size = _check_batch_size(batch_size, oracle)
    first_moment = np.zeros_like(x)
    second_moment = np.zeros_like(x)
    start_time = time()
    history = _init_history(trace, oracle, x, start_time)
    iteration = 0

    for epoch in range(int(max_epoch)):
        samples_seen = 0

        while samples_seen < oracle.m:
            current_batch_size = min(batch_size, oracle.m - samples_seen)
            batch_idx = np.random.choice(
                oracle.m, current_batch_size, replace=False)
            g_k = oracle.grad(x, batch_idx)
            iteration += 1

            first_moment = beta1 * first_moment + (1 - beta1) * g_k
            second_moment = beta2 * second_moment + (1 - beta2) * (g_k ** 2)

            m_hat = first_moment / (1 - beta1 ** iteration)
            v_hat = second_moment / (1 - beta2 ** iteration)
            x -= step_size * m_hat / (np.sqrt(v_hat) + eps)
            samples_seen += current_batch_size

        _save_history(history, oracle, x, epoch + 1, start_time)
        if display:
            print('Epoch: {}, func: {:.6e}'.format(epoch + 1, oracle.func(x)))

    return x, 'success', history
