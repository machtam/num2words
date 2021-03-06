# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.
# Copyright (c) 2017, Nebras Solutions S.A.R.L.  All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA

from __future__ import division
from __future__ import unicode_literals


from .lang_FR import Num2Word_FR
from .currency_2 import parse_currency_parts, prefix_currency


class Num2Word_FR_TN(Num2Word_FR):

    # TODO Adjectives

    def setup(self):
        Num2Word_FR.setup(self)
        self.precision = 1
    
    CURRENCY_FORMS = {
        'TND': (('dinar', 'dinars'), ('millime', 'millimes')),
        'EUR': (('euro', 'euros'), ('centime', 'centimes')),
        'USD': (('dollar', 'dollars'), ('cent', 'cents')),
        'FRF': (('franc', 'francs'), ('centime', 'centimes')),
        'GBP': (('livre', 'livres'), ('penny', 'pence')),
        'CNY': (('yuan', 'yuans'), ('fen', 'jiaos')),
    }
    
    def to_currency(self, val, currency='TND', cents=True, separator=' et',
                    adjective=False):
        """
        Args:
            val: Numeric value
            currency (str): Currency code
            cents (bool): Verbose cents
            separator (str): Cent separator
            adjective (bool): Prefix currency name with adjective
        Returns:
            str: Formatted string

        """
        left, right, is_negative = parse_currency_parts(val)

        try:
            cr1, cr2 = self.CURRENCY_FORMS[currency]

        except KeyError:
            raise NotImplementedError(
                'Currency code "%s" not implemented for "%s"' %
                (currency, self.__class__.__name__))

        if adjective and currency in self.CURRENCY_ADJECTIVES:
            cr1 = prefix_currency(self.CURRENCY_ADJECTIVES[currency], cr1)

        minus_str = "%s " % self.negword if is_negative else ""
        cents_str = self._cents_verbose(right, currency) \
            if cents else "%02d" % right

        return u'%s%s %s%s %s %s' % (
            minus_str,
            self.to_cardinal(left),
            self.pluralize(left, cr1),
            separator,
            cents_str,
            self.pluralize(right, cr2)
        )
