package main

import (
	"context"
	"errors"
	"time"
 "crypto/tls"
	"go.opentelemetry.io/otel"
//	"go.opentelemetry.io/otel/exporters/stdout/stdoutmetric"
//	"go.opentelemetry.io/otel/exporters/stdout/stdouttrace"
	"go.opentelemetry.io/otel/propagation"
//	"go.opentelemetry.io/otel/sdk/metric"
	"go.opentelemetry.io/otel/sdk/resource"
	"go.opentelemetry.io/otel/sdk/trace"
	semconv "go.opentelemetry.io/otel/semconv/v1.24.0"
 	"go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp"
	 "go.opentelemetry.io/otel/attribute"
"encoding/base64" 
    // "crypto/x509"
    "fmt"
    // "io/ioutil"
)

// setupOTelSDK bootstraps the OpenTelemetry pipeline.
// If it does not return an error, make sure to call shutdown for proper cleanup.
func setupOTelSDK(ctx context.Context, serviceName, serviceVersion string) (shutdown func(context.Context) error, err error) {
	var shutdownFuncs []func(context.Context) error

	// shutdown calls cleanup functions registered via shutdownFuncs.
	// The errors from the calls are joined.
	// Each registered cleanup will be invoked once.
	shutdown = func(ctx context.Context) error {
		var err error
		for _, fn := range shutdownFuncs {
			err = errors.Join(err, fn(ctx))
		}
		shutdownFuncs = nil
		return err
	}

	// handleErr calls shutdown for cleanup and makes sure that all errors are returned.
	handleErr := func(inErr error) {
		err = errors.Join(inErr, shutdown(ctx))
	}

	// Set up resource.
	res, err := newResource(serviceName, serviceVersion)
	if err != nil {
		handleErr(err)
		return
	}

	// Set up propagator.
	prop := newPropagator()
	otel.SetTextMapPropagator(prop)

	// Set up trace provider.- user-defined
	tracerProvider, err := newTraceProvider(res,ctx)
	if err != nil {
		handleErr(err)
		return
	}
	shutdownFuncs = append(shutdownFuncs, tracerProvider.Shutdown)
	otel.SetTracerProvider(tracerProvider)

	// Set up meter provider.

/*
	meterProvider, err := newMeterProvider(res)
	if err != nil {
		handleErr(err)
		return
	}
	shutdownFuncs = append(shutdownFuncs, meterProvider.Shutdown)
	otel.SetMeterProvider(meterProvider)
 */

	return
}

func newResource(serviceName, serviceVersion string) (*resource.Resource, error) {

	// projectName := "Banking"
	// appName := "flowlogs"
	// profileKey :="RLgmVLU7Vzi9mtbO6hKxtuKnXeU1/3OrxKu0dJqOCtq9TSHzCGBH0t/h7y0Lf4E6RhGu/RxWCZUTZ08tDKkEbFRVIZrPgwDYEketyBkiFEhJ7Gw1bFqKPqMk+9ZuHbOKesk/5TrSLQDK+S+OdI23mRvwqkaXlFoy5ifIdpDYaYP0yh1XxE7zEvEgCwAzyfujd08NIndes1sNXdVjBuNmnVvDuI6XXHx1YhBnfwpQZnpQXe964bgo4FBvG2MGhiEw6fv4YjRytq4uxMJQ/UmkO8PCa6YyW7kqI79OxWmF0gt4SqJ9g1t/rAKoYfAWCy1+P0I+6Gpz2uZ90rCDQMW7J/wyVZwGt+jUEG+dHgalLKWCrUKwSnbFzuBORaaYiCwyDCTcPeOPm8Y0n9uradBJsbVVFJnrPt6OTVI/Pb/JHHOlH+eJgLN59QamqujliZRVZoWmKTjiHWVHTSJUKBnzoZlwPjL/5uMilz9tKQfPoUrXvPr8UIWW6AauDETYB5K+TipBr9GLmjmKCPZZb6iZR0S+Y8QlXcqcA3GOyfERul6hqYnC5Zk744YCFaGygwvFZlOl4SdfkGJ8w9eCsQ/wMx+JEN0ZN7MTTU1zYsgek8Qdj08uuOymtuKTC2+LvIct68fTk+/l5WEwTJbtShlxPM13vMXjy88l5M22lWgvI1qU4NH45AlG8ETDDDNQtjg9dqbfhqfoPj1DMHuMeLl3maDoUlgvpuffE9PNJX3HVVPZNr1SmRyNX7mmvZJrveBLjFyTgNZWMKsW2T15OBIRIvin+XdaLDWG8lxRmVEY3GoaUxU4MzrtUhcoWG3LoPa76WfAZEY97DI2H2uT7Z/cP+DogbNwgtcHDey9DuvAanMka8x8u3HEs8tqABYejJQ1vbWUBttAYAY0AePPlN0A9w=="
	projectName := "test"
    appName := "test"
    profileKey := "LiF70Ps5ve5Gx1kb3BUm5dIVTRdNm3UbRRdCKiy5AAP1dAEWsp2PjpEfQ83debX+2NiQAeuXblA2cIMcyAEwYyqN5E2yCmX6oiwLL38/SkHThNYGByd5VPcuNukJH+UEJRgaGEWiHJReL7Hjr3zcao/Kw+y3DquDflWY0A43Z3CIeiysBGFmlBXiHI+77LPotGkep2F/DDM1MFQOaGumfg5n3U2rDSVQacNMRhbihPZgZIjkGgeWprXjLRCADj4fI/u4LF/r+quMOzHz62qjTmrPrH3nt1HaWp72WFEK9zC6CbzN8iZ9ld1x3pVPUb3IItT0LK5D499S+EMwTQolvMs2VD//wbzHfJwgpeJcEtiL5/EgqzcWoohiWG2eIyrK2mNTU5kHxnjd7WnG4hpmQpeBvK5UTfI456TYNzN18ON0Z1cwZdsdC4AL580a8FlewLjILJ2Wh988RDVK+j7K8Vc3m6pHQ20VUQo0GMO4+ToJJIsr2Sr1oMgE5662rx5cB6nnxAXlc6i2mtj8qQDbFw+QCicEj/d1y8QcPkSJ39O2bhMC8/C10BO5DKtxOaXrX6/LIPBeLepH8b0xWi5Z/eqxBmTVHERH9MJ8RizjYKlyo3TOdpK8wfDmedtWdnrq"

	return resource.Merge(resource.Default(),
		resource.NewWithAttributes(semconv.SchemaURL,
			semconv.ServiceName(serviceName),
			semconv.ServiceVersion(serviceVersion),
			attribute.String("snappyflow/projectname", projectName),
		attribute.String("snappyflow/appname", appName),
		attribute.String("snappyflow/profilekey", profileKey),
		))
}

func newPropagator() propagation.TextMapPropagator {
	return propagation.NewCompositeTextMapPropagator(
		propagation.TraceContext{},
		propagation.Baggage{},
	)
}

func newTraceProvider(res *resource.Resource,ctx context.Context) (*trace.TracerProvider, error) {
//	traceExporter, err := stdouttrace.New(
//		stdouttrace.WithPrettyPrint())

//user-defined

traceExporter, err := newExporter(ctx)

	if err != nil {
		return nil, err
	}

	traceProvider := trace.NewTracerProvider(
		trace.WithBatcher(traceExporter,
			// Default is 5s. Set to 1s for demonstrative purposes.
			trace.WithBatchTimeout(time.Second)),
		trace.WithResource(res),
	)
	return traceProvider, nil
}


func newTLSConfig() (*tls.Config, error) {
    // cert, err := tls.LoadX509KeyPair("/opt/sfagent/otel-trace-data-forwarder/certs/agent.pem", "/opt/sfagent/otel-trace-data-forwarder/certs/agent-key.pem")
    // if err != nil {
    //     return nil, fmt.Errorf("Error loading X.509 key pair: %v", err)
    // }

    // // Load CA certificate
    // caCert, err := ioutil.ReadFile("/opt/sfagent/otel-trace-data-forwarder/certs/ca.pem")
    // if err != nil {
    //     return nil, fmt.Errorf("Error loading CA certificate: %v", err)
    // }
    // caCertPool := x509.NewCertPool()
    // caCertPool.AppendCertsFromPEM(caCert)

    // // Create a TLS configuration
    // tlsConfig := &tls.Config{
    //     Certificates: []tls.Certificate{cert},
    //     RootCAs:      caCertPool,
    // }
    // return tlsConfig, nil

	tlsConfig := &tls.Config{
		InsecureSkipVerify: true,
	}

	return tlsConfig, nil

}


func newExporter(ctx context.Context) (trace.SpanExporter, error) {


credentials := "otelforwarderuser:Forwarder-Snappyflow-Agent@7$"
encodedCredentials := base64.StdEncoding.EncodeToString([]byte(credentials))
headers := map[string]string{
    "Authorization": "Basic " + encodedCredentials,
}
//user-defined 
    tlsConfig,err := newTLSConfig()
    
    if err != nil {
        return nil, fmt.Errorf("Error loading CA certificate: %v", err)
    }
    
	return otlptracehttp.New(ctx,
 otlptracehttp.WithHeaders(headers),
 otlptracehttp.WithTLSClientConfig(tlsConfig))
  //otlptracehttp.WithInsecure())
}
/*

func newMeterProvider(res *resource.Resource) (*metric.MeterProvider, error) {
	metricExporter, err := stdoutmetric.New()
	if err != nil {
		return nil, err
	}

	meterProvider := metric.NewMeterProvider(
		metric.WithResource(res),
		metric.WithReader(metric.NewPeriodicReader(metricExporter,
			// Default is 1m. Set to 3s for demonstrative purposes.
			metric.WithInterval(3*time.Second))),
	)
	return meterProvider, nil
}

*/
