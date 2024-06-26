from bls.scheme import *


def test_threshold_authorities():
	m = [3] * 2 # messages
	t, n = 19, 20 # number of authorities
	params = setup()

	# generate key
	(sk, vk) = ttp_keygen(params, t, n)

	# aggregate verification keys
	aggr_vk = aggregate_vk(params, vk)

	# sign
	sigs = [sign(params, ski, m) for ski in sk]

	# aggregate credentials
	sigs[1] = None
	sigma = aggregate_sigma(params, sigs)

	# verify signature
	assert verify(params, aggr_vk, sigma, m)


def test_multi_authorities():
	m = [3] * 2 # messages
	n = 3 # number of authorities
	params = setup()

	# generate key
	(sk, vk) = ttp_keygen(params, n, n)

	# aggregate verification keys
	aggr_vk = aggregate_vk(params, vk, threshold=False)

	# sign
	sigs = [sign(params, ski, m) for ski in sk]

	# aggregate credentials
	sigma = aggregate_sigma(params, sigs, threshold=False)

	# verify signature
	assert verify(params, aggr_vk, sigma, m)

def test_distinct_messages_with_multi_authorities():
	m = [10,20,30,40,50]
	n = 5 # number of authorities
	params = setup()

	# generate key
	(sk, vk) = ttp_keygen(params, n, n)

	# sign
	sigs = [sign_unique(params, ski, [mi]) for ski,mi in zip(sk,m)]

	# aggregate credentials
	sigma = aggregate_sigma(params, sigs, threshold=False)

	assert aggregate_verify(params, vk, sigma, m)