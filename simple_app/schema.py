import json 
import graphene

from graphene_django.types import DjangoObjectType
from graphql_relay.node.node import from_global_id
from .models import Message


class MessageType(DjangoObjectType):

    class Meta:
        model = Message
        interfaces = (graphene.Node, )


class CreateMessageMutation(graphene.Mutation):
    
    status = graphene.Int()
    form_errors = graphene.String()
    message = graphene.Field(MessageType)

    @staticmethod
    def mutate(root, info, **kwargs):
        if not info.context.user.is_authenticated:
            return CreateMessageMutation(status=403)
        message = kwargs['message'].strip()

        if not message:
            return CreateMessageMutation(
                status=400,
                form_errors=json.dumps(
                    {'message':[ 'please enter a message',]}
                )
            )
        obj = Message.objects.create(
            user=info.context.user, message=message
        )
        return CreateMessageMutation(status=200, message=obj)

    class Input:
        message = graphene.String()


class Mutation(graphene.AbstractType):
    create_message = CreateMessageMutation.Field()


class Query(graphene.AbstractType):

    all_messages = graphene.List(MessageType)
    message = graphene.Field(MessageType, id=graphene.ID())

    def resolve_all_messages(self, info, **kwargs):
        return Message.objects.all()

    def resolve_message(self, info, **kwargs):
        rid = from_global_id(kwargs['id'])
        return Message.objects.get(pk=rid[1])