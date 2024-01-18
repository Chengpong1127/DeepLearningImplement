import numpy as np


class Tensor:
    def __init__(self, data, requires_grad=True):
        from .module import Module
        self.data = np.array(data, dtype=np.float32)
        self.grad: Tensor = None
        self.grad_fn: Module = None
        self.requires_grad = requires_grad
        
    @property
    def shape(self):
        return self.data.shape
        
    def __add__(self, other):
        from .operations import Add
        return Add()(self, other)
        
    def __sub__(self, other):
        from .operations import Add
        return Add()(self, other * -1)
        
    def __mul__(self, other):
        from .operations import Mul
        return Mul()(self, other)
    
    def __truediv__(self, other):
        from .operations import Mul, Pow
        r_other = Pow()(other, -1)
        return Mul()(self, r_other)
    
    def __pow__(self, other):
        from .operations import Pow
        return Pow()(self, other)
    
    def __matmul__(self, other):
        from .operations import MatMul
        return MatMul()(self, other)
        
    def backward(self, grad=None):
        from .module import Module
        if not self.requires_grad:
            return
        if grad is None:
            grad = Tensor(np.ones_like(self.data))
            
        if not isinstance(grad, Tensor):
            grad = Tensor(grad)
        
        if self.grad is None:
            self.grad = grad
        else:
            self.grad += grad
        if issubclass(type(self.grad_fn), Module):
            self.grad_fn.backward(grad)
                
    def __str__(self):
        return f'Tensor({self.data}, shape = {self.data.shape})'