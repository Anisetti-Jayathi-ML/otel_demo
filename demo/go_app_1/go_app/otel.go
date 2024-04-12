package main

import (
    "context"
    "errors"
    "time"
    "crypto/tls"
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/propagation"
    "go.opentelemetry.io/otel/sdk/resource"
    "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.21.0"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp"
    "encoding/base64" 
    "fmt"
	"go.opentelemetry.io/otel/attribute"
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

    // Set up trace provider.
    tracerProvider, err := newTraceProvider(res,ctx)
    if err != nil {
        handleErr(err)
        return
    }
    shutdownFuncs = append(shutdownFuncs, tracerProvider.Shutdown)
    otel.SetTracerProvider(tracerProvider)

    return
}

func newResource(serviceName, serviceVersion string) (*resource.Resource, error) {
    // TODO: Add Project name , Application name and profile key here.

	configFile := "/home/administrator/demo/go_app_1/go_app/env.conf"
	return resource.NewWithAttributes(
        semconv.SchemaURL,
        semconv.ServiceName(serviceName),
        semconv.ServiceVersion(serviceVersion),
        attribute.String("configFile", configFile),
    ),nil
}

func newPropagator() propagation.TextMapPropagator {
    return propagation.NewCompositeTextMapPropagator(
        propagation.TraceContext{},
        propagation.Baggage{},
    )
}

func newTraceProvider(res *resource.Resource,ctx context.Context) (*trace.TracerProvider, error) {

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
    
	tlsConfig := &tls.Config{
		InsecureSkipVerify: true,
	}

	return tlsConfig, nil
}


func newExporter(ctx context.Context) (trace.SpanExporter, error) {

    // these are default credentials for otel-data-forwarder

    credentials := "otelforwarderuser:Forwarder-Snappyflow-Agent@7$"
    encodedCredentials := base64.StdEncoding.EncodeToString([]byte(credentials))
    headers := map[string]string{
        "Authorization": "Basic " + encodedCredentials,
    }

    tlsConfig,err := newTLSConfig()

    if err != nil {
        return nil, fmt.Errorf("Error loading CA certificate: %v", err)
    }

    return otlptracehttp.New(ctx,
                             otlptracehttp.WithHeaders(headers),
                             otlptracehttp.WithTLSClientConfig(tlsConfig))
}