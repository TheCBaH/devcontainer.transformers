"""Fresh-process execution: intentionally imports only torch, never Transformers."""
import json
import sys

import torch


def main():
    torch.set_num_threads(1)
    payload = torch.load(sys.argv[2], weights_only=True)
    program = torch.export.load(sys.argv[1])
    module = program.module()
    atol, rtol = payload['tolerances']
    with torch.no_grad():
        for case in payload['cases']:
            actual = module(**case['inputs'])
            expected = case['outputs']
            assert isinstance(actual, tuple) and len(actual) == len(expected)
            for left, right in zip(actual, expected, strict=True):
                assert left.shape == right.shape and left.dtype == right.dtype
                assert torch.isfinite(left).all() and torch.isfinite(right).all()
                torch.testing.assert_close(left, right, atol=atol, rtol=rtol)
    assert 'transformers' not in sys.modules
    print(json.dumps({'status': 'ok', 'cases': len(payload['cases']), 'transformers_imported': False}))


if __name__ == '__main__':
    main()
