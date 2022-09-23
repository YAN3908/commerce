from rest_framework import serializers

from auctions.models import Lot


class LotSerializer(serializers.ModelSerializer):
    userLot = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Lot
        # fields = ('lot_name', 'description', 'starting_price', 'price', 'picture', 'image', 'category', 'userLot', 'user_comit', 'time_lot', 'time_sales')
        fields = "__all__"

