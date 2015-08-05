"""Base Class for all Custom Objects, highly based on sklearn Base Class"""
#Author: Miguel Molero <miguel.molero@gmail.com>

import inspect
import six
import numpy as np

def _pprint(params, offset=0, printer=repr):
    """Pretty print the dictionary 'params'
    Parameters
    ----------
    params: dict
        The dictionary to pretty print
    offset: int
        The offset in characters to add at the begin of each line.
    printer:
        The function to convert entries to strings, typically
        the builtin str or repr
    """
    # Do a multi-line justified repr:
    options = np.get_printoptions()
    np.set_printoptions(precision=5, threshold=64, edgeitems=2)
    params_list = list()
    this_line_length = offset
    line_sep = ',\n' + (1 + offset // 2) * ' '
    for i, (k, v) in enumerate(sorted(six.iteritems(params))):
        if type(v) is float:
            # use str for representing floating point numbers
            # this way we get consistent representation across
            # architectures and versions.
            this_repr = '%s=%s' % (k, str(v))
        else:
            # use repr of the rest
            this_repr = '%s=%s' % (k, printer(v))
        if len(this_repr) > 500:
            this_repr = this_repr[:300] + '...' + this_repr[-100:]
        if i > 0:
            if (this_line_length + len(this_repr) >= 75 or '\n' in this_repr):
                params_list.append(line_sep)
                this_line_length = len(line_sep)
            else:
                params_list.append(', ')
                this_line_length += 2
        params_list.append(this_repr)
        this_line_length += len(this_repr)

    np.set_printoptions(**options)
    lines = ''.join(params_list)
    # Strip trailing space to avoid nightmare in doctests
    lines = '\n'.join(l.rstrip(' ') for l in lines.split('\n'))
    return lines


###############################################################################

class BaseObject(object):
    """Base Class for all the Custom Objects in pcloudpy, highly inspired by sklearn Base Class

    Notes
    -----
    All Custom Objects should specify all the parameters that can be set
    at the class level in their ''__init__'' as explicit keyword arguments
    (no ''*args'' pr ''**kwargs).
    """

    @classmethod
    def _get_param_names(cls):

        init = cls.__init__
        if init is object.__init__:
            # No explicit constructor to introspect
            return []

        args, varargs, kw, default = inspect.getargspec(cls.__init__)
        if varargs is not None:
            raise RuntimeError("pcloudpy objects should always "
                               "specify their parameters in the signature"
                               "of their __init__ (no varargs)."
                               " %s doesn't follow this convention."
                               % (cls, ))

        args.pop(0)
        args.sort()
        return args



    def get_params(self, deep=True):
        """Get parameters for this object.

        Parameters
        ----------
        deep: boolean, optional
            If True, will return the parameters for this pcloudpy Object and
            contained sub-objects that are pcloudpy Objects.

        Returns
        -------
        params : mapping of string to any
            Parameter names mapped to their values.
        """

        out = dict()
        for key in self._get_param_names():

            value = getattr(self, key, None)

            if deep and hasattr(value, 'get_params'):
                deep_items = value.get_params().items()
                out.update((key + '__' + k, val) for k, val in deep_items)
            out[key] = value
        return out



    def set_params(self, **params):
        """Set the parameters of this Object.
        The method works on simple pcloudpy Objects.

        Returns
        -------
        self
        """

        if not params:
            # Simple optimisation to gain speed (inspect is slow)
            return self

        valid_params = self.get_params(deep=True)
        for key, value in six.iteritems(params):
            split = key.split('__', 1)
            if len(split) > 1:
                # nested objects case
                name, sub_name = split
                if name not in valid_params:
                    raise ValueError('Invalid parameter %s for object %s' %
                                     (name, self))
                sub_object = valid_params[name]
                sub_object.set_params(**{sub_name: value})
            else:
                # simple objects case
                if key not in valid_params:
                    raise ValueError('Invalid parameter %s ' 'for object %s'
                                     % (key, self.__class__.__name__))
                setattr(self, key, value)
        return self

    def __repr__(self):
        class_name = self.__class__.__name__
        return '%s(%s)' % (class_name, _pprint(self.get_params(deep=False),
                                               offset=len(class_name),),)

