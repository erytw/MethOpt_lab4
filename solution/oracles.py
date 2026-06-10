import numpy as np


_MAX_EXP_ARGUMENT = 700.0


def _stable_exp(values):
    return np.exp(np.clip(values, a_min=None, a_max=_MAX_EXP_ARGUMENT))


class BaseStochasticOracle(object):
    """
    Базовый класс для стохастических оракулов.
    Оценивает функцию и градиент по подвыборке (мини-батчу).
    """

    @property
    def m(self):
        """Возвращает объем обучающей выборки (число объектов)."""
        raise NotImplementedError('Property m is not implemented.')

    def func(self, x, batch_idx=None):
        """
        Вычисляет значение функции потерь на батче (или на всей выборке).
        
        Parameters
        ----------
        x : np.array
            Точка, в которой вычисляется функция.
        batch_idx : np.array of ints or None
            Индексы объектов батча. Если None, функция вычисляется по всей выборке.
            
        Returns
        -------
        f : float
            Значение функции (включая L2-регуляризацию!).
        """
        raise NotImplementedError('Func is not implemented.')

    def grad(self, x, batch_idx=None):
        """
        Вычисляет стохастический градиент на батче (или полный градиент).
        
        Parameters
        ----------
        x : np.array
            Точка, в которой вычисляется градиент.
        batch_idx : np.array of ints or None
            Индексы объектов батча. Если None, вычисляется полный градиент.
            
        Returns
        -------
        g : np.array
            Вектор (стохастического) градиента (включая градиент L2-регуляризатора!).
        """
        raise NotImplementedError('Grad is not implemented.')


# ==============================================================================
# Model-specific Stochastic Oracles
# ==============================================================================

class StochasticClassificationOracle(BaseStochasticOracle):
    """
    Оракул для задачи классификации с экспоненциальной функцией потерь
    (вариант из ЛР №1) и L2-регуляризацией:
    F(x) = (1/m) sum L(y_i <a_i, x>) + (l2_coef/2) ||x||_2^2
    """
    def __init__(self, A, b, l2_coef=0.0):
        """
        Parameters
        ----------
        A : np.array / scipy.sparse matrix
            Матрица признаков (размер m x n).
        b : np.array
            Вектор целевых переменных (размер m).
        l2_coef : float
            Коэффициент L2-регуляризации.
        """
        self.A = A
        self.b = b
        self.l2_coef = l2_coef
        self._m = A.shape[0]

    @property
    def m(self):
        return self._m

    def func(self, x, batch_idx=None):
        if batch_idx is None:
            A_batch = self.A
            b_batch = self.b
        else:
            A_batch = self.A[batch_idx]
            b_batch = self.b[batch_idx]

        y = np.where(np.asarray(b_batch).ravel() > 0, 1.0, -1.0)
        margins = y * A_batch.dot(x)
        loss = np.mean(_stable_exp(-margins))
        reg = 0.5 * self.l2_coef * np.dot(x, x)
        return loss + reg

    def grad(self, x, batch_idx=None):
        if batch_idx is None:
            A_batch = self.A
            b_batch = self.b
        else:
            A_batch = self.A[batch_idx]
            b_batch = self.b[batch_idx]

        y = np.where(np.asarray(b_batch).ravel() > 0, 1.0, -1.0)
        margins = y * A_batch.dot(x)
        coeffs = -y * _stable_exp(-margins)
        grad = A_batch.T.dot(coeffs) / y.size
        return np.asarray(grad).ravel() + self.l2_coef * x


class StochasticRegressionOracle(BaseStochasticOracle):
    """
    Оракул для задачи регрессии с функцией потерь Log-Cosh
    (вариант из ЛР №1) и L2-регуляризацией:
    F(x) = (1/m) sum L(<a_i, x> - b_i) + (l2_coef/2) ||x||_2^2
    """
    def __init__(self, A, b, l2_coef=0.0):
        self.A = A
        self.b = b
        self.l2_coef = l2_coef
        self._m = A.shape[0]

    @property
    def m(self):
        return self._m

    def func(self, x, batch_idx=None):
        if batch_idx is None:
            A_batch = self.A
            b_batch = self.b
        else:
            A_batch = self.A[batch_idx]
            b_batch = self.b[batch_idx]

        residuals = A_batch.dot(x) - np.asarray(b_batch).ravel()
        loss = np.mean(np.logaddexp(residuals, -residuals) - np.log(2.0))
        reg = 0.5 * self.l2_coef * np.dot(x, x)
        return loss + reg

    def grad(self, x, batch_idx=None):
        if batch_idx is None:
            A_batch = self.A
            b_batch = self.b
        else:
            A_batch = self.A[batch_idx]
            b_batch = self.b[batch_idx]

        residuals = A_batch.dot(x) - np.asarray(b_batch).ravel()
        grad = A_batch.T.dot(np.tanh(residuals)) / residuals.size
        return np.asarray(grad).ravel() + self.l2_coef * x
