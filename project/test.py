from django.http import QueryDict

op = {'subparams[0][name]': ['erfeeg'], 'subparams[0][type_subparam]': ['1'], 'subparams[1][name]': ['323'], 'subparams[1][type_subparam]': ['2'], 'csrfmiddlewaretoken': ['R5XPRK4f9sir9VhKwgitJxyQiaBGWf7HznW2R8Xs72oreKRzOgmJn1dJynjZKi9m'],}

query_dict = QueryDict('', mutable=True)
query_dict.update(op)

print(query_dict.popitem())