'''
This file is part of python-libdeje.

python-libdeje is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

python-libdeje is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with python-libdeje.  If not, see <http://www.gnu.org/licenses/>.
'''

from __future__ import absolute_import
from ejtp.identity.core import Identity

identities = {
    "mitzi":("mitzi@lackadaisy.com", ["rsa","-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQDAZQNip0GPxFZsyxcgIgyvuPTHsruu66DBsESG5/Pfbcye3g4W\nwfg+dBP3IfUnLB4QXGzK42BAd57fCBXOtalSOkFoze/C2q74gYFBMvIPbEfef8yQ\n83uoNkYAFBVp6yNlT51IQ2mY19KpqoyxMZftxwdtImthE5UG1knZE64sIwIDAQAB\nAoGAIGjjyRqj0LQiWvFbU+5odLGTipBxTWYkDnzDDnbEfj7g2WJOvUavqtWjB16R\nDahA6ECpkwP6kuGTwb567fdsLkLApwwqAtpjcu96lJpbRC1nq1zZjwNB+ywssqfV\nV3R2/rgIEE6hsWS1wBHufJeqBZtlkeUp/VEx/uopyuR/WgECQQDJOaFSutj1q1dt\nNO23Q6w3Ie4uMQ59rWeRxXA5+KjDZCxrizzo/Bew5ZysJzHB2n8QQ15WJ7gTSjwJ\nMQdl/7SJAkEA9MQG/6JivkhUNh45xMYqnMHuutyIeGE17QndSfknU+8CX9UBLjsL\nw1QU+llJ3iYfMPEDaydn0HJ8+iinyyAISwJAe7Z2vEorwT5KTdXQoG92nZ66tKNs\naVAG8NQWH04FU7tuo9/C3uq+Ff/UxvKB4NDYdcM1aHqa7SEir/P4vHjtIQJAFKc9\n1/BB2MCNqoteYIZALj4HAOl+8nlxbXD5pTZK5UAzuRZmJRqCYZcEtiM2onIhC6Yq\nna4Tink+pnUrw24OhQJBAIjujQS5qwOf2p5yOqU3UYsBv7PS8IitmYFARTlcYh1G\nrmcIPHRtkxIwNuFxy3ZRRPEDGFa82id5QHUJT8sJbqY=\n-----END RSA PRIVATE KEY-----"], ['local', None, 'mitzi']),
    "atlas":("atlas@lackadaisy.com", ["rsa","-----BEGIN RSA PRIVATE KEY-----\nMIICXgIBAAKBgQCvCM8MTSOSeA8G62b9Fg2Ic18JoHoswqn7kmU+qmYxJnTd0rSS\nYaQWiSflchTBgGcbItR4jsktYifOSfp7Cl1k5IHXqGKLHtIt8Fo02k/ajR5DzGJN\n2yAJfbBCi43ifOaVKwjuJqcFKhuPUqNJecFn8m62QOQehrIlUAlnnM7OXQIDAQAB\nAoGBAJGrVRU5xZcKUAdENkv+5Hhg/AE5CzThNTJnXddPXQkepjhOOXVxyWvv7cIo\ntVltEWImFInY21jnzZUDQHDR6XLCe8B3LRlOWrkv7+byesIFkNH9C7uvheD5xxiG\nzPpOkpwcms3QW+/FmhN5Wia+4oeHB4J9uAjJmNoaddfqAhWBAkEAwdEjMzJaKIx5\n6OIyYAEnC6lvVI6Qx/ssKQH7GhaItxzLZRaIaK4XUgrL5q1OHNNCCFgREw7nhyu3\nZnt8v833rQJBAOcw/wQ0iQktluqKoT4i73hRkGk7MTB2Y/4e2YTVnypUtQC+jxs1\nND3CJj59oJojfA3SJg0M0pWXcMKIIhRxx3ECQQCVl6zafBeYSmxhsgx9iwYu+xSh\np/PZVmTMNeowRYo6AvB90nlwikYXnZupLMQofWnu9MIg+pT7AGPqpo8vn3J1AkAU\nowEAhRf+Y71m7jz6aO/rU4yKeCgp5UeDtYlBHDh69Ni7Wkc37IXfRWdYiKo/WA+I\nxEt1OsHJbJ06ICC6pnVhAkEAio1qXj8vLi9t9xocRe8LIthaYBslw4B8yY69fRhd\nuQifuvld7xjeXsfCWRmA4t72SmcAyzMaG5wnqhLNeCXXYw==\n-----END RSA PRIVATE KEY-----"], ['local', None, 'atlas']),
    "victor":("victor@lackadaisy.com", ["rsa","-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQC6efOadLJZpX837OIpAlqO2NQEfOA1DE8lfC1q8fKGtMlEl8Oq\nR9lbEiMdsbg5M902Gi33UMlJuap+5TaGEBJDBJZNr3d2LFOjlEPGyJeqiu5PnBjX\n3vZx97y+NUm71rsL7k1KRjzAQnuCPSSqQdo5GLdNODgTa2ljXQ4Khd/9CwIDAQAB\nAoGARbSkfQ42RRB6N7uS5uV8WH1w86SCYxIQ2+BJUfrTP8uAmOVqPNLSyxpCii0O\nwkNC46BxoktOkwKWWwzvjrmfOU2hEga3ny/S1r2VU6nfex29ozl+gUD7zEkB8MaV\nQqnRF18gkeGvHcCMU5nSbjYaosp39yj9qBcRDePQIWN3aRECQQDCj8FWSyrP/zoN\n+6YR3j/0Ty6b43KDU3fcvG/+IvHhB+OFawiPlR3uPGYVJG0CfbWC/QEtx90VcGi5\nOnaQRtsXAkEA9VyYg5+5ZzfbfGqZZZRvPHk08rsquAXnGWkT67lobkBtWvx0TxYo\nTKi8PwLZ8paLA3wf2VDJ6/Ufn5APOtSWLQJAP5cUrcurlofoxaE2SijF5mfq5/CT\nAPFK/85nHDz3qYEWkAjHp4YpXjBHfSmGp4XGyaU/uWLVk6hF0iSVk9pUyQJACNya\nSY64RIkY7UpwVeHhjp6WEfo+lbzo1tsbtBTTN8At8u5RSRX0yKgDfIce1gsn5C1U\nfSXU1SfaR4oNcsOA1QJBAKDEQ4PATuH46E7e3Ie+A5AUVSyLqO5H2SC0yg6zduG6\npxbmsfpVLOfko+j9YrH+OdD5WIAjN/wL1CtmVhqSLr8=\n-----END RSA PRIVATE KEY-----"], ['local', None, 'victor']),
}

def identity(name="mitzi"):
    return Identity(*identities[name])
