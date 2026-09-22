from .state import StateFactory

def superpose(branches,amplitudes,**kw):
    return StateFactory.pure(branches,amplitudes,**kw)
