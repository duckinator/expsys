from .inference_engine import InferenceEngine


class PyspreadInterface:
    def __init__(self, S, output_table=0, rules_table=1, agents_table=2):
        self.S = S
        self._output_table = output_table
        self._rules_table = rules_table
        self._agents_table = agents_table
        self.values = {}

    def update(self):
        inf = InferenceEngine(self.agents, self.rules)
        num_matched = 0
        for row_number, row_data in enumerate(self.S[1:, :, self._rules_table]):
            row = row_number + 1
            name, _expression, watched, explanation, _unused_column = row_data
            if name is None:
                print(f'[{row}] name is None. Stopping.')
                break

            if not watched:
                continue

            print(f'Checking status for: {name!r}')
            status = inf[name]

            if status:
                print(f'row = {row!r}; name = {name!r}')
                num_matched += 1
                self.S[row, 0, self._output_table] = repr(name)
                self.S[row, 1, self._output_table] = repr(explanation)
                self.S[row, 2, self._output_table] = repr(inf.status(name)[1])
            else:
                print(f'row = {row!r}; name = {name!r}')
                self.S[row, 0, self._output_table] = ''
                self.S[row, 1, self._output_table] = ''
                self.S[row, 2, self._output_table] = ''
        if num_matched == 0:
            self.S[1, 0, self._output_table] = repr('No rules were matched.')

    @property
    def agents(self):
        return dict(filter(lambda row: row.any(), self.S[1:, :2, self._agents_table]))

    @property
    def rules(self):
        return dict(filter(lambda row: row.any(), self.S[1:, :2, self._rules_table]))
