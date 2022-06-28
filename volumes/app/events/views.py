from operator import and_
from functools import reduce
from datetime import datetime

from django.http import Http404
from django.db.models import Q

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated

from events.models import Events
from events.serializers import EventSerializer



class EventList(generics.ListAPIView):
    """"
    balance list
    /events/?strategy=GAMMA&symbol=BTCUSDT&from=1612345678911&to=1612345678911&limit=30
    """
    serializer_class    = EventSerializer
    permission_classes  = (IsAuthenticated,)

    def get_queryset(self):
        userId      = self.request.user.id
        strategy    = self.request.query_params.get('strategy')
        symbol      = self.request.query_params.get('symbol')
        fromTime    = self.request.query_params.get('from')
        toTime      = self.request.query_params.get('to')
        limit       = self.request.query_params.get('limit')

        l = [fromTime,toTime]     

        for i in range(len(l)):
            if l[i] is not None:
                try:
                    l[i] = datetime.fromtimestamp(int(l[i])/1000)
                except:
                    raise APIException("invalid query parameters(from|to).")

        if limit is None:
            limit = 30
        else:
            try:
                limit = int(limit)
            except:
                raise APIException("invalid query parameters(limit).")

        Qlist=[
            Q(profile__user__id=userId),
            Q(symbol=symbol),
            Q(strategy__strategy=strategy),
            Q(createTime__gte=fromTime),
            Q(createTime__lte=toTime)
        ]

        return Events.objects.filter(reduce(and_, [q for q in Qlist if q.children[0][1] is not None])).order_by('-createTime')[:limit]
    
    def list(self,requests):
        queryset = self.get_queryset()
        serializer = EventSerializer(queryset, many=True)  
        if queryset.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_200_OK)

