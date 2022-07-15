import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3Assets from 'aws-cdk-lib/aws-s3-assets'
import * as elasticbeanstalk from 'aws-cdk-lib/aws-elasticbeanstalk';
import * as iam from 'aws-cdk-lib/aws-iam'
import { PolicyStatement } from 'aws-cdk-lib/aws-iam';


export class UfcPredictorInfraStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // Construct an S3 asset from the ZIP located from directory up.
    const webAppZipArchive = new s3Assets.Asset(this, 'WebAppZip', {
      path: `${__dirname}/../app.zip`,
    });

    // Create a ElasticBeanStalk app.
    const appName = 'UfcEventPredictor';
    const app = new elasticbeanstalk.CfnApplication(this, 'Application', {
      applicationName: appName,
    });
    // Create an app version from the S3 asset defined earlier
    const appVersionProps = new elasticbeanstalk.CfnApplicationVersion(this, 'AppVersion', {
      applicationName: appName,
      sourceBundle: {
        s3Bucket: webAppZipArchive.s3BucketName,
        s3Key: webAppZipArchive.s3ObjectKey,
      },
    });
    // Make sure that Elastic Beanstalk app exists before creating an app version
    appVersionProps.addDependsOn(app);

    // Create role and instance profile
    const myRole = new iam.Role(this, `${appName}-aws-elasticbeanstalk-ec2-role`, {
      assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com'),
    });
    const managedPolicy = iam.ManagedPolicy.fromAwsManagedPolicyName('AWSElasticBeanstalkWebTier')

    myRole.addManagedPolicy(managedPolicy)
    myRole.addToPolicy(new PolicyStatement({
      resources: ['*'],
      actions: ["secretsmanager:GetSecretValue"],

    }))

    const myProfileName = `${appName}-InstanceProfile`

    const instanceProfile = new iam.CfnInstanceProfile(this, myProfileName, {
      instanceProfileName: myProfileName,
      roles: [
        myRole.roleName
      ]
    });

    // Example of some options which can be configured
    const optionSettingProperties: elasticbeanstalk.CfnEnvironment.OptionSettingProperty[] = [
      {
        namespace: 'aws:autoscaling:launchconfiguration',
        optionName: 'IamInstanceProfile',
        value: myProfileName,
      },
      {
        namespace: 'aws:autoscaling:asg',
        optionName: 'MinSize',
        value: '1',
      },
      {
        namespace: 'aws:autoscaling:asg',
        optionName: 'MaxSize',
        value: '1',
      },
      {
        namespace: 'aws:ec2:instances',
        optionName: 'InstanceTypes',
        value: 't2.micro',
      },
      {
        namespace: "aws:elasticbeanstalk:application:environment",
        optionName: "FLASK_APP",
        value: "application"
      },
      {
        namespace: "aws:elasticbeanstalk:application:environment",
        optionName: "FLASK_ENV",
        value: "dev"
      },
    ];

    // Create an Elastic Beanstalk environment to run the application
    const elbEnv = new elasticbeanstalk.CfnEnvironment(this, 'Environment', {
      environmentName: 'UfcEventPredictorEnv',
      applicationName: app.applicationName || appName,
      solutionStackName: '64bit Amazon Linux 2 v3.3.14 running Python 3.8',
      optionSettings: optionSettingProperties,
      versionLabel: appVersionProps.ref,
    });
  }
}
