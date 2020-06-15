from time import sleep
import json
import boto3
import RPi.GPIO as GPIO


GPIO_CHANNEL = 8
RELAY_OPEN = GPIO.LOW
RELAY_CLOSED = GPIO.HIGH
PUMP_INTERVAL = 20
SNS_TOPIC="arn:aws:sns:eu-central-1:718527891033:ACTIVATE_PUMP"


def open_relay():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GPIO_CHANNEL, GPIO.OUT)
    GPIO.output(GPIO_CHANNEL, RELAY_OPEN)
    sleep(PUMP_INTERVAL)
    GPIO.output(GPIO_CHANNEL, RELAY_CLOSED)


def notify():
    with open('config.json') as f:
        config = json.load(f)

    sns = boto3.client('sns')
    sns.publish(TopicArn=SNS_TOPIC,
                Subject='waterpi ran the pump',
                Message='waterpi ran the pump'
                )


def main():
    try:
        open_relay()
        notify()
    finally:
        GPIO.cleanup()



if __name__ == "__main__":
    main()
