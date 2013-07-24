from mamba import describe, context, before

from sure import expect
from doublex import *

from mamba import reporters
from mamba.spec import Spec


with describe(reporters.Reporter) as _:
    @before.each
    def create_new_test():
        def _test():
            _.was_run = True

        _.was_run = False
        _.test = Spec(_test)

    with context('when running an spec'):
        @before.each
        def run_test():
            _.reporter = Spy(reporters.Reporter)
            _.test.run(_.reporter)

        def it_notifies_that_a_spec_is_started():
            assert_that(_.reporter.spec_started, called().with_args(_.test))

        with context('when ran successfully'):
            def it_notifies_is_passed():
                assert_that(_.reporter.spec_passed, called().with_args(_.test))

        with context('when ran failed'):
            def _failing_test():
                raise ValueError()

            def it_notifies_is_failed():
                _.test = Spec(_failing_test)

                _.test.run(_.reporter)

                assert_that(_.reporter.spec_failed, called().with_args(_.test))

        with context('when spec is pending'):
            def it_notifies_is_pending():
                _.test.pending = True

                _.test.run(_.reporter)

                assert_that(_.reporter.spec_pending, called().with_args(_.test))