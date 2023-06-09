import torch
import string

all_char = string.printable
n_all_char = len(all_char)
all_categories = ["normal", "attack"]


def char2index(char: str):
    return all_char.find(char)


def char2tensor(char: str):
    tensor = torch.zeros(1, n_all_char)
    tensor[0][char2index(char)] = 1
    return tensor


def line2tensor(line: str):
    tensor = torch.zeros(len(line), n_all_char)
    for i, char in enumerate(line):
        tensor[i][char2index(char)] = 1
    return tensor


def categoryFromOutput(output):
    top_n, top_i = output.topk(1)
    category_i = top_i[0].item()
    return all_categories[category_i], category_i


class RNN(torch.nn.Module):
    def __init__(
        self, input_size=n_all_char, hidden_size=128, output_size=2, num_layers=2
    ):
        super().__init__()

        self.num_layers = num_layers
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.rnn = torch.nn.RNN(
            input_size=self.input_size,
            hidden_size=self.hidden_size,
            num_layers=num_layers,
        )
        self.h2o = torch.nn.Linear(hidden_size, output_size)

    def forward(self, input):
        hidden = torch.zeros(self.num_layers, self.hidden_size)
        input, _ = self.rnn(input, hidden)
        output = self.h2o(input[-1, :])
        return output.unsqueeze(0)


class RNNSentinel:
    def __init__(self, pt_path: str):
        super().__init__()
        self.rnn = RNN()
        checkpoint = torch.load(pt_path)
        self.rnn.load_state_dict(checkpoint["state"])

    def evaluate(self, path):
        test_tensor = line2tensor(path)
        category, category_i = categoryFromOutput(self.rnn(test_tensor))
        return category_i


if __name__ == "__main__":
    rnn = RNNSentinel(pt_path="30w.pt")
