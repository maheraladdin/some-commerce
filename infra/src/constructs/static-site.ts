import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import * as origins from 'aws-cdk-lib/aws-cloudfront-origins';
import * as s3deploy from 'aws-cdk-lib/aws-s3-deployment';
import { Construct } from 'constructs';

export interface StaticSiteProps {
  /** Identifier for the site, e.g. 'storefront' or 'dashboard' */
  siteName: string;
  /** Local path to the static build output directory (e.g. apps/<app>/dist) */
  buildOutputDir: string;
  /** Optional custom domain name (e.g. store.some-commerce.com) */
  customDomain?: string;
  /** Optional ACM certificate ARN */
  certificateArn?: string;
}

/**
 * Reusable AWS CDK Construct for deploying SPA / static sites
 * backed by an encrypted S3 bucket, CloudFront distribution with Origin Access Control (OAC),
 * SPA client-side routing fallback (403/404 -> index.html), and S3 BucketDeployment.
 */
export class StaticSiteConstruct extends Construct {
  public readonly bucket: s3.Bucket;
  public readonly distribution: cloudfront.Distribution;
  public readonly siteUrl: string;

  constructor(scope: Construct, id: string, props: StaticSiteProps) {
    super(scope, id);

    // 1. S3 Bucket for static assets (Strictly private with OAC)
    this.bucket = new s3.Bucket(this, 'SiteBucket', {
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      encryption: s3.BucketEncryption.S3_MANAGED,
      enforceSSL: true,
      removalPolicy: cdk.RemovalPolicy.RETAIN,
      versioned: true,
    });

    // 2. CloudFront Origin Access Control (OAC) backed distribution
    this.distribution = new cloudfront.Distribution(this, 'SiteDistribution', {
      defaultBehavior: {
        origin: origins.S3BucketOrigin.withOriginAccessControl(this.bucket),
        viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        allowedMethods: cloudfront.AllowedMethods.ALLOW_GET_HEAD,
        cachedMethods: cloudfront.CachedMethods.CACHE_GET_HEAD,
        compress: true,
        cachePolicy: cloudfront.CachePolicy.CACHING_OPTIMIZED,
      },
      defaultRootObject: 'index.html',
      // Client-side SPA routing fallback (redirects client routes to index.html with 200 OK)
      errorResponses: [
        {
          httpStatus: 403,
          responseHttpStatus: 200,
          responsePagePath: '/index.html',
          ttl: cdk.Duration.seconds(0),
        },
        {
          httpStatus: 404,
          responseHttpStatus: 200,
          responsePagePath: '/index.html',
          ttl: cdk.Duration.seconds(0),
        },
      ],
      priceClass: cloudfront.PriceClass.PRICE_CLASS_100,
      httpVersion: cloudfront.HttpVersion.HTTP2_AND_3,
      comment: `some-commerce ${props.siteName} static site CDN`,
    });

    // 3. S3 Bucket Deployment: Synchronizes dist/ folder and invalidates CloudFront cache
    new s3deploy.BucketDeployment(this, 'SiteDeployment', {
      sources: [s3deploy.Source.asset(props.buildOutputDir)],
      destinationBucket: this.bucket,
      distribution: this.distribution,
      distributionPaths: ['/*'],
      prune: true,
    });

    this.siteUrl = `https://${this.distribution.distributionDomainName}`;

    // 4. CloudFormation Outputs
    new cdk.CfnOutput(this, `${props.siteName}BucketName`, {
      value: this.bucket.bucketName,
      description: `S3 storage bucket for ${props.siteName} static site`,
    });

    new cdk.CfnOutput(this, `${props.siteName}DistributionId`, {
      value: this.distribution.distributionId,
      description: `CloudFront distribution ID for ${props.siteName}`,
    });

    new cdk.CfnOutput(this, `${props.siteName}Url`, {
      value: this.siteUrl,
      description: `Live CloudFront URL for ${props.siteName} static site`,
    });
  }
}
